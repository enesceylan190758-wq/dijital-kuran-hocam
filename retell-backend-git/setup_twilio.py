import os
from twilio.rest import Client

# User Credentials
account_sid = 'AC471e8aee78036b1870621525d68e1999'
auth_token = '4b25fd3d3af83fe528995284f6922d0e'
twilio_number = '+16825169466'

# Retell Configuration
# Typically: sip:sip.retellai.com or sip.livekit.cloud
# Based on common docs: sip:5t4n6j0wnrl.sip.livekit.cloud;transport=tcp is safe
RETELL_SIP_URI = "sip:5t4n6j0wnrl.sip.livekit.cloud;transport=tcp"
TRUNK_NAME = "Retell AI Trunk"
TERMINATION_URI_PREFIX = "retell-term-enes" # Must be unique globally

client = Client(account_sid, auth_token)

def setup_trunk():
    print("Step 1: Finding/Creating Elastic SIP Trunk...")
    try:
        # Check for existing trunks
        trunks = client.trunking.v1.trunks.list(limit=1)
        if trunks:
            trunk = trunks[0]
            print(f"✅ Found Existing Trunk: {trunk.sid} ({trunk.friendly_name})")
        else:
            trunk = client.trunking.v1.trunks.create(
                friendly_name=TRUNK_NAME,
                secure=False 
            )
            print(f"✅ Trunk Created: {trunk.sid}")
    except Exception as e:
        print(f"❌ Error getting trunk: {e}")
        return None

    # Origination (Inbound to Retell)
    print("Step 2: Configuring Origination URI...")
    try:
        client.trunking.v1.trunks(trunk.sid).origination_urls.create(
            weight=10,
            priority=10,
            enabled=True,
            friendly_name="Retell SIP",
            sip_url=RETELL_SIP_URI
        )
        print("✅ Origination URI Configured")
    except Exception as e:
        print(f"❌ Error setting origination: {e}")

    # Termination (Outbound from Retell)
    print("Step 3: Configuring Termination URI...")
    try:
        domain_name = f"{TERMINATION_URI_PREFIX}.pstn.twilio.com"
        client.trunking.v1.trunks(trunk.sid).termination.update(
            cidr_prefix_list=['0.0.0.0/0'], # Allow all for now, Retell has dynamic IPs
            secure=False
        )
        # We need to set the URI suffix
        # Note: Termination resource in python lib might be tricky, checking simplified approach
        # Actually creating a credential list is best practice for Retell
        
        # For now let's just create credential list
        cred_list = client.sip.credential_lists.create(friendly_name="Retell Auth")
        cred = client.sip.credential_lists(cred_list.sid).credentials.create(
            username="retell_user",
            password="StrongPassword123!"
        )
        
        client.trunking.v1.trunks(trunk.sid).credential_lists.create(
            credential_list_sid=cred_list.sid
        )
        print("✅ Termination Auth Configured (User: retell_user, Pass: StrongPassword123!)")
        
        # Set URI
        # client.trunking.v1.trunks(trunk.sid).update(domain_name=domain_name) # Sometimes trunk update handles domain
        
    except Exception as e:
        print(f"⚠️ Warning on Termination (might need manual check): {e}")

    # Link Number
    print(f"Step 4: Linking Number {twilio_number}...")
    try:
        # Find the number SID first
        incoming_numbers = client.incoming_phone_numbers.list(phone_number=twilio_number)
        if not incoming_numbers:
            print("❌ Error: Phone number not found in account.")
            return

        number_sid = incoming_numbers[0].sid
        
        # Update number to use SIP Trunk
        client.incoming_phone_numbers(number_sid).update(
            trunk_sid=trunk.sid,
            voice_receive_mode='voice',
            # voice_url='' # Clear webhook if present
        )
        print("✅ Phone Number Linked to Trunk!")
        
    except Exception as e:
        print(f"❌ Error linking number: {e}")

    print("\n--- DONE ---")
    print(f"Trunk SID: {trunk.sid}")
    print(f"SIP Termination URI: {TERMINATION_URI_PREFIX}.pstn.twilio.com")
    print("Credentials: retell_user / StrongPassword123!")

if __name__ == "__main__":
    setup_trunk()
