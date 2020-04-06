# Zestaw 1 (Grafy i ich zastosowania)

## Jak użyć lab01
Dla dokładnych możliwości użycia: 
``` bash
./lab01 -h
```
Przykładowe use-case'y
``` bash
./lab01.py --load lab01.al --save al am im png
./lab01.py -n 10 -p 0.5 --save al
./lab01.py -n 9 -l 25 --save png
```
## Polecenie
1. Napisać program kodujący grafy proste za pomocą macierzy sąsiedztwa, macierzy incydencji i list sąsiędztwa. Stworzyć moduł do zmiany
danego kodowania na pozostałe.

2. Napisać program do wizualizacji grafów prostych używający reprezentacji, w której wierzchołki grafu są równomiernie rozłożone na okręgu.

3. Napisać program do generowania grafów losowych G(n, l) oraz G(n, p).

- G(n, l)
	- n - liczba wierzchołków
	- l - liczba krawędzi
- G(n, p)
	- n - liczba wierzchołków
	- p - prawdopodobieńswto istnienia krawędzi (z prawdopodobieństwem *p* dokładamy krawędź przy iterowanie po każdej mozliwej krawędzi)