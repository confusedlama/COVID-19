### Markov-Ketten: Epidemiemodellierung

#### Lernziele für heute

* Verstehen was eine Markov-Kette ist
* Verstehen welche Systeme man durch Markov-Ketten beschreiben kann
* Mit Hilfe von einer Markov-Kette die Entwicklung von einer Epedemie simulieren
* Die Simulation evaluieren

#### Markov-Ketten

Markov-Ketten sind ein Werkzeug mit dem man zufallsbasierte Vorgänge modellieren kann. Eine Markov-Kette besteht aus einer Menge an Zuständen, in denen das modellierte Sytsem sich zu unterschiedlichen Zeiten befinden kann, und Übergangswahrscheinlichkeiten für alle Paare von Zuständen aus dieser Menge. Markov-Ketten eignen sich gut um Systeme zu beschreiben, deren Veränderung nur von ihrem derzeitigen Zustand und nicht ihrer Vergangenheit abhängt.

<b>Beispiel:</b>
<p align="center">
    <img src="Markov-Chain_example.svg">
</p>
Zustandsmenge:

{Z1, Z2, Z3}


Übergangswahrscheinlichkeiten:
| P | Z1 | Z2 | Z3 |
|---|----|----|----|
| Z1'| P(Z1'\|Z1) | P(Z2'\|Z1) | 0 |
| Z2'| 0 | 0 | P(Z3'\|Z2) |
| Z3'| 0 | 0 | P(Z3'\|Z3) |

Zwei wichtige Adjektive die man kennen muss um Markov-Ketten zu verstehen sind "diskret", oder "abzählbar". Diskret und abzählbar haben beide die gleiche Bedeutung und beschreiben Mengen. Eine diskrete Menge hat entweder endlich viele Elemente, oder man kann ihre Elemente abzählen, so dass man nach beliebig viel Zeit allen Elementen eine Nummer zugeteilt hat. Zwei diskrete Mengen wären Beispielweise: {b, c, a, d}, oder {1, 2, 3, 4, ...}. Ein Beispiel für eine nicht-diskrete Menge wären die Reellen Zahlen, also alle Zahlen mit beliebig (auch unendlich) vielen Nachkommastellen. Auch wenn das kein formal richtiger Beweis ist, kann man sich als Intuition, warum sie nicht diskret sind, vorstellen, dass es zwischen zwei beliebigen Reellen Zahlen immer unendlich viele andere Reelle Zahlen gibt. Das Gegenteil von diskret heißt kontinuierlich.

Die Menge der Zustände einer Markov-Kette muss diskret sein. Außerdem soll heute die Menge an Zeitpunkten, an denen unser System seinen Zusand wechseln kann, auch diskret sein.


##### Aufgabe 1 Was heißt diskret?

Diskutieren sie mit ihrem Sitznachbar, ob folgende Mengen diskret sind:

1. Die Menge der Sekunden in einer Minute
2. Die Menge der Zeitpunkte in einer Minute
3. Die Menge der Städte in Europa
4. Die Menge der Orte (im Sinne von Platz) auf der Erde

##### Aufgabe 2 Was lässt sich mit Markov-Ketten modellieren?

Untersuchen sie zusammen mit ihrem Sitznachbar die folgenden Systeme darauf, ob sie sich gut durch eine Markov-Kette beschreiben lassen. Insbesondere sollen sie betrachten, ob der Zustandsraum und die Zeitpunkte zu denen das System beschrieben wird diskret sind, so wie, ob die Übergangswahrscheinlichkeit zwischen Zuständen nur vom derzeitigen, oder auch von zukünftigen Zuständen abhängt.

1. Ein System das kontinuierlich den Ort eines durch die Luft fliegenden Balls angibt
2. Ein System das jede Sekunde den Ort eines durch die Luft fliegenden Balls angibt
3. Ein System das jede Sekunde die abgerundete Distanz in Metern die ein Ball zurücklegt der durch Luft fliegt angibt
4. Ein System das jede Sekunde die abgerundete Distanz und Geschwindigkeit in Metern bzw. Metern pro Sekunde die ein Ball zurücklegt der durch Vakuum fliegt angibt

#### Epidemiemodellierung

Wir wollen eine Epidemie mit Hilfe von einer Markov-Kette modellieren, also die Entwicklung der Gesunden, Infizierten, Verstorbenen und Genesenen Personen vorhersagen. Da es einfacher ist setzen wir uns nur das Ziel die gesamten Gesunden, Infizierten, etc. nach n Tagen vorherzusagen. Eine weitere Vereinfachung die wir treffen ist, dass Genesene nicht wieder "gesund" werden, bzw. nicht ein zweites Mal krank werden können. Als Beispiel verwenden wir die Corona Epedemie in Deutschland, da es hierzu relativ aktuelle Statistiken gibt. Die Daten die wir verwenden wollen stammen von der Johns Hopkins University und sind in folgendem [Git Repository](https://github.com/confusedlama/COVID-19) im Ordner "data" hinterlegt.

Die Daten sind wie folgt aufgebaut:

| date    | healthy | infected | recovered | infected_cumulated | deceased | 
| -------- | ------- | ----------|----------|---------|-----------|
| 1/23/20  | 82 500 000   | 0 | 0 | 0 | 0 |

* "<b> date </b>" ist das Datum zu dem die restlichen Daten der Reihe gehören. *str(Datetime)*

* "<b> healthy </b>" ist die Anzahl der Personen, die sich noch nicht mit Corona angesteckt haben. *int*

* "<b> infected </b>" ist die Anzahl der Personen die momentan mit dem Virus infiziert sind. *int*

* "<b> recovered </b>" ist die Anzahl der Personen die infiziert waren und dann genesen sind. *int*

* "<b> deceased </b>" ist die Anzahl der Personen die als an Corona verstorben gemeldet wurden nachdem sie infiziert waren. *int*

* "<b> infected_cumulated </b>" ist die Anzahl der Personen die insgesamt mit Corona infiziert waren. *int*

##### Aufgabe 3 Ein erster Blick in die Daten.

* Beginnen sie damit das Git Repository zu clonen, und erstellen sie ein neues Jupyter Notebook.
* Laden sie die .csv datei von Deutschland in ihrem Jupyter Notebook als DataFrame
* Visualisieren sie sich den DataFrame

```python
# Code Beispiel für die Visualisierung eines DataFrames in einem Jupyter Notebook
df.plot()
```

##### Aufgabe 4 Wie sieht unsere Zustandsmenge aus?
* Überlegen sie mit ihrem Sitznachbarn, ob die Zustände in der Zustandsmenge der Markov-Kette der Verteilung der Gesamtbevölkerung über die unterschiedlichen Kategorien (gesund, infiziert, ...), oder den Zuständen in denen eine einzelne Person sich befinden kann entsprechen sollten.
* Schreiben sie die Zustandsmenge ihrer Markov-Kette auf. Ist sie diskret?
* In welchen zeitlichen Abständen sind die einzelnen Datenpunkte in ihrem DataFrame aufgenommen, bzw. wird die Entwicklung der Fallzahlen zu diskreten Zeitpunkten betrachtet?
* Die Übergangswahrscheinlichkeiten zu den anderen Zuständen der Zustandsmenge sollten nur vom aktuellen Zustand abhängen. Schätzen sie wovon die Zahlen des nächsten Tages jeweils abhängen. (nur ganz grob die Trends)
* Zeichnet ein Diagram eurer Markov-Kette mit ihren Zuständen und Pfeilen zwischen den Zuständen falls die Übergangswahrscheinlichkeit größer als 0 ist.

##### Aufgabe 5 Was sind unsere Übergangswahrscheinlichkeiten?
Wir vermerken die Übergangswahrscheinlichkeiten in einer Matrix P:

Übergangswahrscheinlichkeiten:
| P | H | I | R | D |
|---|----|----|----| ---|
| H'| P(H'\|H) | P(H'\|I) | P(H'\|R) | P(H'\|D) |
| I'| P(I'\|H)  | P(I'\|I) | P(I'\|R) | P(I'\|D) |
| R'| P(R'\|H)  | P(R'\|I) | P(R'\|R) | P(R'\|D) |
| D'| P(D'\|H)  | P(D'\|I) | P(D'\|R) | P(D'\|D) |

Sie sollen nun die Übergangswahrscheinlichkeiten zwischen ihren Zuständen berechnen. Die echten Wahrscheinlichkeiten zu berechnen ist relativ schwer. Beispielsweise wäre die Wahrscheinlichkeit, dass ein gesunder Mensch infiziert wird abhängig von der Wahrscheinlichkeit, dass ein gesunder Mensch einen infizierten Menschen trifft und der Wahrscheinlichkeit, dass ein infizierter Mensch einen Gesunden Menschen ansteckt wenn sie sich treffen. Diese Wahrscheinlichkeiten können wir nicht berechnen, da wir keine Daten dazu haben, wie sich die Bevölkerung bewegt, bzw. wie ansteckend infizierte Personen sind. Stattdessen müssen wir eine Heuristik finden, also eine Wahrscheinlichkeit die die echte Übergangswahrscheinlichkeit abschätzt. Eine sinnvolle Heuristik stellen wir jetzt vor:

Aus den Daten von der JHU die wir gestellt haben betrachten wir alle Paare von Tagen die aufeinanderfolgen, wie zum Beispiel 12-01-2021 und 13-01-2021. Tag1 nennen wir immer jeweils den ersten Tag aus den Paaren und Tag2 den darauf folgenden. Wir markieren die Daten die zu Tag2 gehören mit einem Strich:

Tag1: gesund, infiziert, genesen, verstorben
Tag2: gesund', infiziert', genesen', verstorben'

Jetzt wollen wir für zwei Zustände A, B' jeweils über alle Paare von Tagen den mittleren Anteil der Menschen aus A finden der am nächsten Tag in B' ist.

<b>Beispiel:</b>
A = gesund, B' = infiziert'
c = np.array mit jeweils der Anzahl der Menschen in gesund bei Tag1
d = np.array mit jeweils der Anzahl der Menschen die an Tag1 in gesund waren aber bei Tag2 in infiziert' sind
P(B'|A) = mean( d / c )

<b> Achtung: </b>
* Durch 0 teilen ist nicht zulässig
* Die ausgehenden Wahrscheinlichkeiten an einem Zustand müssen insgesamt 1 sein 

##### Aufgabe 6 Wie macht man einen Simulationsschritt?
Als nächstes wollen wir mit Hilfe von P unsere Simulation implementieren. Unser Ziel ist es die Anzahl der Gesunden, Infizierten, Genesenen und Verstorbenen nach n Tagen für bestimmte Start Werte vorher zu sagen. Um die neuen Werte für den jeweils nächsten Tag zu berechnen führt man folgende Rechnung durch:

für die Vektoren
$\overrightarrow{a}$ = [|Gesund|, |Infiziert|, |Genesen|, |Verstorben|]
$\overrightarrow{b}$ = [|Gesund'|, |Infiziert'|, |Genesen'|, |Verstorben'|]

P * $\overrightarrow{a}$ = $\overrightarrow{b}$

Wenn man also die Vorhersage für n = 10 haben möchte muss man 10 mal diese Rechnung durchführen.

* Schreiben sie die Matrixmultiplikation aus und versuchen sie nach zu vollziehen warum man so die Vorhersage für den nächsten Tag berechnen kann.
* Implementieren sie den Simulationsschritt

##### Aufgabe 7 Evaluation
* Speichern Sie alle $\overrightarrow{a}$ und $\overrightarrow{b}$ die Sie berechnen in ein np.array und fügen sie sie dem DataFrame als neue Spalten hinzu. Das heißt die Vorhersagen für z.B. infiziert stehen dann alle in einer Spalte "vorhersagen_infiziert" im DataFrame.

##### Aufgabe 8 (Bonus) Herumspielen mit dem Model