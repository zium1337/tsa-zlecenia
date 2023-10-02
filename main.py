import io
import setup
import pendulum as pen
import db


class Program:
    def __init__(self):
        self.database, self.connect = setup.check()
        self.dir = "C:/Program Files (x86)/MTA San Andreas 1.6/MTA/logs"

    def zliczanie(self):
        db.Database().drop()
        for i in range(0, 6):
            if i == 0:
                log = io.open(f"{self.dir}/console.log", mode="r",
                              encoding="utf-8", errors="ignore")
            else:
                log = io.open(f"{self.dir}/console.log.{i}", mode="r",
                              encoding="utf-8", errors="ignore")
            for j in log:
                if "Twoje aktualne zlecenie:" in j:
                    data = j.replace('[', '').replace(']', '')[:19]
                    gracz = log.readline().rsplit(' ', 4)[2] + ' '
                    self.connect.execute(f"SELECT COUNT(czas) FROM zlecenia WHERE czas='{data}'")
                    data = pen.parse(data)
                    if self.connect.fetchall()[0][0] == 0:
                        if pen.now(tz='Europe/Warsaw').previous(6).add(hours=21) < data.in_timezone(
                                tz='Europe/Warsaw') < pen.now(tz='Europe/Warsaw').next(6).add(hours=21):
                            db.Database().dodanie(gracz, data.to_datetime_string())
                    else:
                        print(
                            f"Znaleziono już takie zlecenie w tym tygodniu! Pomijam.\nData: {data.to_datetime_string()}")
        Program().podliczenie()

    def podliczenie(self):
        self.connect.execute("SELECT COUNT(nick) FROM zlecenia WHERE NOT nick='placeholder'")
        i = self.connect.fetchall()[0][0]
        print(f"\nLiczba wykonanych zleceń w tym tygodniu wynosi: {i}")


if __name__ == '__main__':
    Program().zliczanie()
