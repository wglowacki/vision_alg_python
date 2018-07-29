
Metryka Hausdorfa
1. Cel zaj��
zapoznanie z zagadnieniem por�wnywania kontur�w obiekt�w z wykorzystaniem metryki Hausdorfa
2. Obliczanie odleg�o�ci Hausdorffa dla pary kontur�w
2.1.Ze strony kursu pobierz archiwum z danymi do �wiczenia i rozpakuj je we w�asnym katalogu roboczym.

2.2. Utw�rz nowy skrypt. Wczytaj obraz 'imgs/c_astipalea.bmp' i zmie� jego typ na 'graylevel'.  Wykorzystaj funkcj� cv2.findContours do uzyskania kontur�w wyst�pujacych na obrazie (Uwaga - zaneguj obraz przed przes�aniem go do funkcji, gdy� zawiera on czarny kontur na bia�um tle, a funkcja findContours oczekuje odwrotnego ustawienia). Zwr�� uwag�, aby uzyska� listy wszystkich punkt�w konturu (parametr CHAIN_APPROX_NONE).

Wynikiem funkcji jest m.in. lista kontur�w (teoretycznie na obrazie mo�e by� wi�cej obiekt�w), w naszym wypadku powinna to by� lista jednoelementowa. Uzyskany kontur mo�na nanie�� na dowolny obraz funkcj�   cv2.drawContours( image, contours, 0, color) gdzie image to obraz docelowy, contours - lista kontur�w,  0 - numer konturu, color - jasno�� lub krotka ze sk�adowymi koloru (w zale�no�ci od typu obrazu)

2.3. Zaimplementuj funkcj� tworz�c� na podstawie konturu c dwie tablice (lub listy) z osobno wsp�rz�dnymi x i y jego punkt�w. Funkcja powinna otrzymywa� jako parametr kontur z funkcji findContours. Tablice ze wsp�rz�dnymi mo�na 'wyci�gn��' z parametru poleceniami:

x=c[:,0,0]

y=c[:,0,1]

gdzie c- kontur z findContours, x, y - tablice wsp�rz�dnych

Dla uniezale�nienia si� od obrot�w nale�y 'uwsp�lni�' �rodek obrotu. W tym celu przelicz wsp�rz�dne w obu tablicach tak, aby punkt (0,0) znalaz� si� w �rodku ci�ko�ci analizowanego obiektu (czyli odejmnij od wsp�rz�dnych z obu tablic wsp�rz�dne �rodka ci�ko�ci). Do wyznaczenia �rodka ci�ko�ci mo�na wykorzysta� momenty centralne 'm00', 'm10' i 'm01'.  (funkcja cv2.moments(c, 1)). Aby uniezale�ni� si� od rozmiaru znormalizuj rozmiar obiektu przez podzielenie wsp�rz�dnych z obu tablic przez najwi�ksz� odleg�o�� pomi�dzy punktami konturu (wylicz t� odleg�o�� w p�tli/p�tlach po obu tablicach). Niech dodatkowo funkcja zwraca wyliczone  wsp�rz�dne �rodka ci�ko�ci (przydadz� si� p�niej)

2.4. Zaimplementuj funkcj� wyliczaj�c� odleg�o�� Hausdorfa mi�dzy dwoma znormalizowanymi konturami uzyskanymi z poprzedniej funkcji (czyli  zapisanymi jako dwie tablice ze wsp�rz�dnymi x i y ka�dego z konturu�w) Innymi s�owy funkcja otrzyma 4 tablice (listy) wsp�rz�dnych.  Funkcja powinna wyliczy� odleg�o�� jako wi�ksz� z dw�ch odleg�o��i: dH+ i dH- . Niech odleg�o�� pomi�dzy punktami niech b�dzie liczona jako odleg�o�� Euklidesowa.

2.4.Sprawdzimy poprawno�� dzia�ania funkcji poprzez policzenie odleg�o�ci Hausdorffa mi�dzy wczytanym ju� obiektem a wszystkimi obiektami zapisanymi w katalogu imgs. Uruchom funkcj� wyliczaj�c� znormalizowany kontur dla uczytanego obiektu (ithaca). Aby wczyta� wszystkie pliki z folderu imgs  zaimportuj modu� os i wywo�aj funcj� os.listdir('imgs') - zwr�ci ona list� wszystkich plik�w z tego katalogu. Nast�pnie w p�tli po tej li�cie odtw�rz nazwy ze �cie�k�:

nazwa_ze_sciezka = 'imgs/' + nazwa_z_listy

aby wczyywa� pliki zobiektami i dla ka�dego z nich znajd� kontury (findContures) oraz ruchom funkcj� wyliczaj�c� znormalizowany kontur a nast�pnie  wylicz odleg�o�� Hausdorffa od znormalizowanego konturu c_astipalea (zak�adamy, �e ka�dy plik zawiera tylko jeden obiekt, wi�c bierzemy tylko pierwszy znalezziony kontur; prosz� pami�ta� o zanegowaniu obrazu przed wyliczeniem kontur�w). Wyniki zapisuj w tablicy lub li�cie. Po p�tli znajd� indeks najmniejszej odleg�o�ci (metoda argmin tablicy numpy) - je�eli wyniki by�y zapisywane w li�cie przekonwertuj j� na tablic� (tablica = np.array(lista)). Wy�wietl najmniejsz� odleg�o�� i nazw� pliku nazw� pliku kt�ra jej dotyczy. Je�eli wszystko dzia�a poprawnie powinni�my otrzyma� 0 i c_astipalea.bmp.

2.5. Wczytaj  obraz Aegeansea.jpg. Nale�y przekszta�ci� go tak, aby uzyska� obraz binarny - bia�y l�d na czarnym morzu. Zastosuj przej�cie do przestrzeni HSV (cvtColor(imc, cv2.COLOR_BGR2HSV)) Stosunkowo dory wynik mo�na uzyska� binaryzuj�c sk�adow� S z progiem 30 a negacj� sk�adowej H z progiem 60 - iloczyn tych dw�ch binaryzacji daje obraz - map�, kt�r� daje si� wykorzysta� w dalszej cz�sci zadania (cho� zach�cam do znalezienia lepszej jako�ci :)).Wyszukaj kontury na mapie. Odrzu� te kontury, kt�re s� za ma�e lub za du�e (np.

contours = list(filter(lambda el : el.shape[0]>15 and el.shape[0]<3000, contours)) - gdzie contours jest jednym z wynik�w findContours) Dla wszystkich nieodrzuconych kontur�w przeprowad� por�wnanie z astipalea (podobnie jak w poprzednim punkcie - tylko tym razem nie wczytujemy kontur�w z plku tylko bierzemu je z mapy) Uzyskamy indeks najbardziej podobnego konturu. Ale czy znale�li�my w�a�ciw� wysp�? Dla weryfikacji nale�a�oby nanie�� na map� numery (indeksy) kontur�w, aby m�c to sprawdzi�. Mozna wykorzysta� w p�tli nast�puj�ce polecenie:

cv2.putText(obraz_mapy_kolor, str(indeks_konturu),(int(gx),int( gy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(128,128,128)) - gdzie gx, gy to wsp�rz�dne �rodka ci�ko�ci

a dodatkowo po p�tli :

cv2.putText(obraz_mapy_kolor, nazwa_najmniejszego_konturu,(int(gx),int( gy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255))  umie�ci nazw� przy znalezionej wyspie.

Nazw� z nazwy pliku mo�na uzyska� przez:

    nazwa = nazwa_pliku.split('.')[0].split('_')[1]

2.6. Powtarzaj�c operacj� z punktu 2.5 dla ka�dego pliku z katalogi 'imgs' mo�esz spr�bowa� ponazywa� wszystkie wyspy (kt�re usa si� znale��) i por�wna� rezultat z klasyczn� map� Morza Egejskiego.