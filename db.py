import setup
import pendulum as pen


class Database:
    def __init__(self):
        self.db, self.connect = setup.check()

    def dodanie(self, *args):
        self.connect.execute(f"INSERT INTO zlecenia VALUES ('{args[0].replace(' ', '')}', '{args[1]}')")
        self.db.commit()
        print(f"\nDodano zlecenie:\nGracz: {args[0]}\nData: {args[1]}")

    def drop(self):
        self.connect.execute(f"DELETE FROM zlecenia WHERE czas<'{pen.now(tz='Europe/Warsaw').previous(6).add(hours=21).to_datetime_string()}'")
        self.db.commit()
        print("Wyczyszczono bazę ze zleceń z poprzedniego tygodnia!")