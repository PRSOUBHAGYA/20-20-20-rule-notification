from config import UserConfig
from app import MenubarApp
import rumps

def main():
    config = UserConfig()
    app = MenubarApp(config)
    app.run()

if __name__ == "__main__":
    main()
