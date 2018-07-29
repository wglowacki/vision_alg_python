
Metryka Hausdorfa
1. Cel zajêæ
zapoznanie z zagadnieniem porównywania konturów obiektów z wykorzystaniem metryki Hausdorfa
2. Obliczanie odleg³oœci Hausdorffa dla pary konturów
2.1.Ze strony kursu pobierz archiwum z danymi do æwiczenia i rozpakuj je we w³asnym katalogu roboczym.

2.2. Utwórz nowy skrypt. Wczytaj obraz 'imgs/c_astipalea.bmp' i zmieñ jego typ na 'graylevel'.  Wykorzystaj funkcjê cv2.findContours do uzyskania konturów wystêpujacych na obrazie (Uwaga - zaneguj obraz przed przes³aniem go do funkcji, gdy¿ zawiera on czarny kontur na bia³um tle, a funkcja findContours oczekuje odwrotnego ustawienia). Zwróæ uwagê, aby uzyskaæ listy wszystkich punktów konturu (parametr CHAIN_APPROX_NONE).

Wynikiem funkcji jest m.in. lista konturów (teoretycznie na obrazie mo¿e byæ wiêcej obiektów), w naszym wypadku powinna to byæ lista jednoelementowa. Uzyskany kontur mo¿na nanieœæ na dowolny obraz funkcj¹   cv2.drawContours( image, contours, 0, color) gdzie image to obraz docelowy, contours - lista konturów,  0 - numer konturu, color - jasnoœæ lub krotka ze sk³adowymi koloru (w zale¿noœci od typu obrazu)

2.3. Zaimplementuj funkcjê tworz¹c¹ na podstawie konturu c dwie tablice (lub listy) z osobno wspó³rzêdnymi x i y jego punktów. Funkcja powinna otrzymywaæ jako parametr kontur z funkcji findContours. Tablice ze wspó³rzêdnymi mo¿na 'wyci¹gn¹æ' z parametru poleceniami:

x=c[:,0,0]

y=c[:,0,1]

gdzie c- kontur z findContours, x, y - tablice wspó³rzêdnych

Dla uniezale¿nienia siê od obrotów nale¿y 'uwspólniæ' œrodek obrotu. W tym celu przelicz wspó³rzêdne w obu tablicach tak, aby punkt (0,0) znalaz³ siê w œrodku ciê¿koœci analizowanego obiektu (czyli odejmnij od wspó³rzêdnych z obu tablic wspó³rzêdne œrodka ciê¿koœci). Do wyznaczenia œrodka ciê¿koœci mo¿na wykorzystaæ momenty centralne 'm00', 'm10' i 'm01'.  (funkcja cv2.moments(c, 1)). Aby uniezale¿niæ siê od rozmiaru znormalizuj rozmiar obiektu przez podzielenie wspó³rzêdnych z obu tablic przez najwiêksz¹ odleg³oœæ pomiêdzy punktami konturu (wylicz tê odleg³oœæ w pêtli/pêtlach po obu tablicach). Niech dodatkowo funkcja zwraca wyliczone  wspó³rzêdne œrodka ciê¿koœci (przydadz¹ siê póŸniej)

2.4. Zaimplementuj funkcjê wyliczaj¹c¹ odleg³oœæ Hausdorfa miêdzy dwoma znormalizowanymi konturami uzyskanymi z poprzedniej funkcji (czyli  zapisanymi jako dwie tablice ze wspó³rzêdnymi x i y ka¿dego z konturuów) Innymi s³owy funkcja otrzyma 4 tablice (listy) wspó³rzêdnych.  Funkcja powinna wyliczyæ odleg³oœæ jako wiêksz¹ z dwóch odleg³oœæi: dH+ i dH- . Niech odleg³oœæ pomiêdzy punktami niech bêdzie liczona jako odleg³oœæ Euklidesowa.

2.4.Sprawdzimy poprawnoœæ dzia³ania funkcji poprzez policzenie odleg³oœci Hausdorffa miêdzy wczytanym ju¿ obiektem a wszystkimi obiektami zapisanymi w katalogu imgs. Uruchom funkcjê wyliczaj¹c¹ znormalizowany kontur dla uczytanego obiektu (ithaca). Aby wczytaæ wszystkie pliki z folderu imgs  zaimportuj modu³ os i wywo³aj funcjê os.listdir('imgs') - zwróci ona listê wszystkich plików z tego katalogu. Nastêpnie w pêtli po tej liœcie odtwórz nazwy ze œcie¿k¹:

nazwa_ze_sciezka = 'imgs/' + nazwa_z_listy

aby wczyywaæ pliki zobiektami i dla ka¿dego z nich znajdŸ kontury (findContures) oraz ruchom funkcjê wyliczaj¹c¹ znormalizowany kontur a nastêpnie  wylicz odleg³oœæ Hausdorffa od znormalizowanego konturu c_astipalea (zak³adamy, ¿e ka¿dy plik zawiera tylko jeden obiekt, wiêc bierzemy tylko pierwszy znalezziony kontur; proszê pamiêtaæ o zanegowaniu obrazu przed wyliczeniem konturów). Wyniki zapisuj w tablicy lub liœcie. Po pêtli znajdŸ indeks najmniejszej odleg³oœci (metoda argmin tablicy numpy) - je¿eli wyniki by³y zapisywane w liœcie przekonwertuj j¹ na tablicê (tablica = np.array(lista)). Wyœwietl najmniejsz¹ odleg³oœæ i nazwê pliku nazwê pliku która jej dotyczy. Je¿eli wszystko dzia³a poprawnie powinniœmy otrzymaæ 0 i c_astipalea.bmp.

2.5. Wczytaj  obraz Aegeansea.jpg. Nale¿y przekszta³ciæ go tak, aby uzyskaæ obraz binarny - bia³y l¹d na czarnym morzu. Zastosuj przejœcie do przestrzeni HSV (cvtColor(imc, cv2.COLOR_BGR2HSV)) Stosunkowo dory wynik mo¿na uzyskaæ binaryzuj¹c sk³adow¹ S z progiem 30 a negacjê sk³adowej H z progiem 60 - iloczyn tych dwóch binaryzacji daje obraz - mapê, któr¹ daje siê wykorzystaæ w dalszej czêsci zadania (choæ zachêcam do znalezienia lepszej jakoœci :)).Wyszukaj kontury na mapie. Odrzuæ te kontury, które s¹ za ma³e lub za du¿e (np.

contours = list(filter(lambda el : el.shape[0]>15 and el.shape[0]<3000, contours)) - gdzie contours jest jednym z wyników findContours) Dla wszystkich nieodrzuconych konturów przeprowadŸ porównanie z astipalea (podobnie jak w poprzednim punkcie - tylko tym razem nie wczytujemy konturów z plku tylko bierzemu je z mapy) Uzyskamy indeks najbardziej podobnego konturu. Ale czy znaleŸliœmy w³aœciw¹ wyspê? Dla weryfikacji nale¿a³oby nanieœæ na mapê numery (indeksy) konturów, aby móc to sprawdziæ. Mozna wykorzystaæ w pêtli nastêpuj¹ce polecenie:

cv2.putText(obraz_mapy_kolor, str(indeks_konturu),(int(gx),int( gy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(128,128,128)) - gdzie gx, gy to wspó³rzêdne œrodka ciê¿koœci

a dodatkowo po pêtli :

cv2.putText(obraz_mapy_kolor, nazwa_najmniejszego_konturu,(int(gx),int( gy)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255))  umieœci nazwê przy znalezionej wyspie.

Nazwê z nazwy pliku mo¿na uzyskaæ przez:

    nazwa = nazwa_pliku.split('.')[0].split('_')[1]

2.6. Powtarzaj¹c operacjê z punktu 2.5 dla ka¿dego pliku z katalogi 'imgs' mo¿esz spróbowaæ ponazywaæ wszystkie wyspy (które usa siê znaleŸæ) i porównaæ rezultat z klasyczn¹ map¹ Morza Egejskiego.