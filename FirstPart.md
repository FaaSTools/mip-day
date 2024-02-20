# Teil 1

## Schritt 1: Pseudonym überlegen

In den folgenden Schritten werden wir alle auf einem gemeinsamen Account mit geteilten Ressourcen arbeiten.

Dafür ist es notwendig, dass Sie die temporären Dateien und Funktionen die wir in den kommenden Schritten erstellen eindeutig benennen.
Dafür benötigen Sie einen Identifier der Sie eindeutig identifiziert.

Überlegen Sie sich ein Pseudonym oder verwenden Sie Ihren Klarnamen oder eine E-Mail-Adresse. (Bedenken Sie, dass alles was Sie im folgenden von sich preis geben, mehr oder weniger öffentlich ist)

Wenn Sie Hilfe benötigen, können Sie die folgende Seite verwenden:
[https://marc.codeberg.page/docker-name-generator](https://marc.codeberg.page/docker-name-generator/)

## Schritt 2: Log in

Bei der AWS Management Konsole anmelden

[https://717556240325.signin.aws.amazon.com/console](https://717556240325.signin.aws.amazon.com/console)

Die Zugangsdaten können Sie der Präsentation entnehmen.

Stellen Sie sicher, dass die richtige Region ausgewählt ist (Präsentation). 
Die Auswahl ist rechts oben, links von Ihrem Benutzernamen.

## Schritt 3: AWS Lambda

Navigieren Sie über die Suchleiste, oder nach unserer Anleitung zu `Lambda` und machen Sie sich mit der Benutzeroberfläche vertraut. 

## Schritt 4: Funktion erstellen

Wir erstellen nun eine Funktion. Folgen Sie dazu bitte den **exakten** Anweisungen der Vortragenden.

### Funktionsname

Der Name der Funktion **MUSS** dem Schema **mip-day-\<YOUR PSEUDONYM\>** folgen!

Ersetzen Sie \<YOUR PSEUDONYM\> durch das von Ihnen gewählte Pseudonym aus Schritt 1. 

###  Runtime der Funktion

Wählen Sie **Python 3.11**

### Standard-Ausführungsrolle

Wählen Sie **Verwenden einer vorhandenen Rolle**

Suchen und wählen Sie: **mip-day-lambda-role**

**NUR WENN ALLE OBIGEN SCHRITTE KORREKT AUSGEFÜHRT WURDEN, LÄSST SICH DIE FUNKTION ERSTELLEN**

## Schritt 5: Hello World!

### Test ausführen.

Klicken Sie auf Test.

Vergeben Sie einen Ereignis-Name. Dieser kann beliebig sein.

Im Ereignis-JSON, können wir Funktionsparameter angeben.

Überschreiben Sie das Ereignis-JSON mit dem unteren Wert und ersetzen Sie \<YOUR PSEUDONYM\> mit Ihrem Pseudonym aus Schritt 1.

```json
{
    "name": "<YOUR PSEUDONYM>"
}
```

Klicken Sie erneut auf Test.

Die Funktion wird ausgeführt, und gibt aber Hello World from Lambda zurück. 


### Funktion anpassen

Passen Sie die Funktion so an, dass Sie **"Hello \<YOUR PSEUDONYM\> from Lambda"** zurückgibt.

Hinweis 1: 

```python
pseudonym = event['name']
``` 

Hinweis 2: 
```python
# All of the following statements print "Hi du"
print('Hi' + ' ' + 'du')
print('Hi du')
print("Hi " + 'du') 
```

### Funktion deployen und Testen

Drücken Sie auf Deploy und Test.

Wenn Sie alles richtig gemacht haben, gibt die Funktion jetzt Ihr Pseudonym zurück. 

Bevor wir mit dem nächsten Teil weitermachen, gibt es wieder ein wenig Theorie.

