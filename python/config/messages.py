START_MESSAGE = "Ja sam FIPU bot, poslat ću ti svaku novu obavijesti sa oglasne ploče.\n" \
                "Pošalji '/registracija' za primanje obavijesti, ili '/odjava' da ih prestaneš dobivati\n" \
                "Nakon registracije pošalji '/godina N', kako bi notifikacije bile filtrirane s obzirom" \
                " na tvoju godinu\n" \
                "Pošalji '/pomoc' za opis svih naredbi!"

REGISTER_SUCCESS = "Registracija uspješna!"
ALREADY_REGISTERED = "Već si registriran/a!"

UNREGISTER_SUCCESS = "Nisi više registriran/a!"
ALREADY_UNREGISTER = "Već si se odjavio/la od dobivanja obavijesti!"

UPDATE_YEAR_PARAMETER_INVALID = "Krivi format. Očekivani format '/godina 'N', gdje je 'N' broj godine"
UPDATE_YEAR_EXCEEDED = "Najveća godina studija je pet (5)"
UPDATE_YEAR_SUCCESS = "Godina uspješno ažurirana.\nTrenutno odabrana godina je:\n{}"

INFO = "Trenutna odabrana godina:\n{}"

NEED_TO_BE_REGISTERED = "Moraš se prvo registrirati!"

ALL_COMMANDS = "/start - početna poruka\n" \
               "/registracija - registracija na notifikacije\n" \
               "/odjava - odjava sa notifikacija\n" \
               "/godina N - filtiranje notifikacija po godini\n(0 = sve obavijesti, godine = 1-5)\n" \
               "/info - tvoje informacije\n" \
               "/pomoc - popis svih naredbi"
