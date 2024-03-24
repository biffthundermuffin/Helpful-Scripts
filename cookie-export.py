import sqlite3
import os

def find_firefox_profile():
    # Check common locations for Firefox profiles directory
    common_locations = [
        os.path.expanduser('~/.mozilla/firefox'),
        os.path.expanduser('~/Library/Application Support/Firefox/Profiles'),
        os.path.expanduser('~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles')
    ]

    for location in common_locations:
        if os.path.exists(location):
            return location

    return None

def export_cookies_to_netscape(output_dir):
    profiles_dir = find_firefox_profile()

    if profiles_dir is None:
        print("Firefox profiles directory not found.")
        return

    # Look for the profile directory containing 'cookies.sqlite'
    for profile in os.listdir(profiles_dir):
        profile_path = os.path.join(profiles_dir, profile)
        cookies_path = os.path.join(profile_path, 'cookies.sqlite')
        if os.path.isfile(cookies_path):
            cookies_db = cookies_path
            output_file = os.path.join(output_dir, 'cookies.txt')

            conn = sqlite3.connect(cookies_db)
            c = conn.cursor()

            # Query to fetch cookies data from the database
            c.execute("SELECT host, isSecure, path, isSecure, expiry, name, value FROM moz_cookies")

            with open(output_file, 'w') as f:
                for row in c.fetchall():
                    host, isSecure, path, isSecure, expiry, name, value = row
                    # Converting expiry to Unix timestamp
                    expiry = int(expiry)
                    # Formatting the cookie in Netscape format
                    f.write(f"{host}\t{isSecure}\t{path}\t{isSecure}\t{expiry}\t{name}\t{value}\n")

            conn.close()
            return

    print("Firefox profile containing 'cookies.sqlite' not found.")

output_directory = r'c:\scripts'
export_cookies_to_netscape(output_directory)
