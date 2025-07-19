import webview
import subprocess
import webbrowser

# This is the Python object exposed to JavaScript
class API:
    def run_script(self):
        print("Script requested by frontend.")
        subprocess.Popen(["python", "script.py"], shell=True)
        return "Script launched."
    def openDiscord(self):
        print("Open Discord Requested.")
        webbrowser.open_new_tab('https://optb.short.gy/discord')
        return "Check your browser for the discord invite."
    def openDiscord(self):
        print("Open GitHub Page Requested.")
        webbrowser.open_new_tab('https://github.com/OptionallyBlueStudios')
        return "Check your browser for the github page."
    def openCheatSpy(self):
        print("Open GitHub Page Requested.")
        webbrowser.open_new_tab('https://github.com/CheatSpy')
        return "Check your browser for the github page."

if __name__ == '__main__':
    api = API()
    
    # Load your live webpage
    webview.create_window(
        title="BlueHub Launcher",
        url="https://optionallybluestudios.github.io/BlueHub",  # 👈 Change this
        js_api=api,
        width=800,
        height=600
    )
    
    webview.start()
