# Manuell Testplan för applikation

## Översikt

Denna testplan beskriver den manuella testningen av applikationen. Applikationen hanterar information om patienter, vilket inkluderar att lägga till, uppdatera, radera och visa patientdata.

## Förutsättningar

- PySide6 är installerat.
- Alla övriga requirements har installerats.
- Projektet är i en sådan miljö att GUI kan köras och användarinteraktioner kan testas.

## Testfall

### Testfall 1: Grundläggande GUI-laddning

**Beskrivning:** Kontrollera att huvudfönstret kan initialiseras och visas utan fel.

**Steg:**
1. Starta applikationen.
2. Kontrollera att alla flikar visas i huvudfönstret.

**Förväntat resultat:** Huvudfönstret samt alla flikar ska laddas utan att några exceptions kastas, och alla flikar ska visas korrekt.

### Testfall 2: Lägg till patient

**Beskrivning:** Kontrollera att ny patient kan läggas till.

**Steg:**
1. Gå till fliken "Lägg till".
2. Fyll i alla nödvändiga fält.
3. Klicka på "Spara"-knappen.
4. Öppna `csv filen` och verifiera att den nya patienten har lagts till.

**Förväntat resultat:** Den nya patienten ska läggas till i `csv filen`.

### Testfall 3: Radera patient

**Beskrivning:** Kontrollera att en patienten kan raderas.

**Steg:**
1. Gå till fliken "Radera".
2. Välj en patient från rullgardinsmenyn.
3. Klicka på "Radera"-knappen.
4. Öppna `vpl.csv` och verifiera att patienten har tagits bort.

**Förväntat resultat:** Den valda patienten ska raderas från `vpl.csv`.

### Testfall 4: Uppdatera patientdata

**Beskrivning:** Kontrollera att en cell i patientdata kan uppdateras.

**Steg:**

1. Gå till fliken "Uppdatera".
2. Välj en patient och en kolumn från rullgardinsmenyerna.
3. Ange ett nytt värde i textfältet.
4. Klicka på "Spara"-knappen.
5. Öppna `csv filen` och verifiera att cellvärdet har uppdaterats.

**Förväntat resultat:** Cellvärdet ska uppdateras i `csv filen`.

### Testfall 5: Visa patientdata

**Beskrivning:** Kontrollera att patientdata kan visas och sorteras.

**Steg:**
1. Gå till fliken "Visa".
2. Verifiera att tabellen visar korrekt data från `csv filen`.
3. Klicka på olika sorteringsknappar ("Personnummer", "Förnamn", "Efternamn", etc.).
4. Kontrollera att tabellen sorteras korrekt enligt vald kolumn.

**Förväntat resultat:** Tabellen ska visa korrekt data och sorteras korrekt enligt vald kolumn.

### Testfall 6: Uppdatera sidinnehåll

**Beskrivning:** Kontrollera att innehållet på sidan uppdateras korrekt när data ändras.

**Steg:**
1. Uppdatera data i `csv filen` manuellt.
2. Navigera till flikarna "Radera", "Uppdatera", och "Visa".
3. Verifiera att informationen på sidorna återspeglar de senaste ändringarna i CSV-filerna.

**Förväntat resultat:** Sidorna ska visa uppdaterad information som speglar ändringarna i CSV-filerna.

### Testfall 7: Formuläråterställning

**Beskrivning:** Kontrollera att formulärfält återställs korrekt efter åtgärder som spara och radera.

**Steg:**
1. Lägg till en patient från fliken "Lägg till".
2. Verifiera att textfälten och rullgardinsmenyn återställs efter att ha sparat.
3. Radera en patient från fliken "Radera".
4. Verifiera att rullgardinsmenyn återställs efter att ha raderat.

**Förväntat resultat:** Textfälten och rullgardinsmenyn ska återställas efter att ha sparat eller raderat data.

## Slutsats

Jag har testat allt detta och det fungerar som det ska. Under testningens gång upptäckte jag vissa problem som korrigerats.

- Under uppdatera på samtliga sidor finns en rullgardins-meny som kallas "Kolumn". Denna hade "" som ett alternativ. Detta gjorde att om jag klickade utan att ange kolumn, så skapades nya kolumner som sparades i csv filen.
- Jag upptäckte att när jag skulle lägga till en patient på "VPL", så skapades en extra kolumn i csv filen. Detta berodde på att jag har globala variabler som jag av misstag ändrade i koden.