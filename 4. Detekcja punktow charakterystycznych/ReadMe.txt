1. Cel zaj��
zapoznanie z zagadnieniem opisywania punkt�w charakterystycznych
otoczenie punktu jako deskryptor
por�wnanie dzia�ania metody Harrisa i SIFT
2. Prosta deskrypcja punkt�w charakterystycznych
2.1. UWAGA - niniejsze �wiczenie jest kontynuacj� poprzedniego - b�d� w nim potrzebne zar�wno obrazy jak i funkcje z poprzedniego �wiczenia. Ze strony kursu pobierz archiwum z dodatkowymi danymi do �wiczenia i rozpakuj je we w�asnym katalogu roboczym.

2.2. W skrypcie z ubieg�ego tygodnia dodaj funkcj� tworz�c� opisy punkt�w charakterystycznych (w postaci ich otocze�). Jako parametry funkcja powinna otrzyma� obraz, list� wsp�rz�dnych punkt�w charakterystycznych (wynik funkcji z poprzednich zaj��) oraz wielko�� otoczenia.Z listy punkt�w nale�y usun�� wszystkie punkty, kt�rych otoczenia nie mieszcz� si� w obrazie.

Dygresja - mo�na wykorzysta� funkcj� filter z anonimow� funkcj� lambda yx:  yx[0]>=s and yx[0]<Y-s and yx[1]>=s and yx[1]<X-s - przyk�adowo:

lista=list(filter(lambda yx:  yx[0]>=s and yx[0]<Y-s and yx[1]>=s and yx[1]<X-s, lista))   

Nast�pnie nale�y  stworzy� list� opis�w punkt�w po odfiltrowaniu. Opisem b�dzie wycinek obrazu z otoczenia punktu o rozmiarze podanym przez parametr. Przy czym dobrze b�dzie sprowadzi� go do wektora. Je�eli np. p jest wycinkiem, to za pomoc� p.flatten( ) uzyskuje si� z niego wektor. Jako wynik funkcji nale�y zwr�ci� list� otocze� uzupe�nionych o wsp�rz�dne ich punkt�w centralnych.

Dygresja - w tym celu mo�na zzipowa� przefiltrowan� list� wsp�rz�dnych z list� otocze� (funkcja zip) - przyk�adowo 

wynik = list(zip(l_otoczen, l_wspolrzednych)) i zwracamy wynik

2.3. Dodaj funkcj� por�wnuj�c� opisy punkt�w charaktereystycznych z dw�ch obraz�w i znajduj�c� opisy najbardziej podobne. Funkcja jako parametry powinna otrzyma� dwie listy opis�w punkt�w charakterystycznych (z funkcji z p.2.2) oraz liczb� N najbardziej podobnych do siebie opis�w. Funkcja mo�e wykorzysta� metod� 'ka�dy z ka�dym' - ka�dy opis punktu z listy pierwszej jest por�wnywany ze wszystkimi opisami z listy drugiej i wybierany jest opis najbardziej podobny. Mo�na r�nie okre�li� miar� podobie�stwa.  Mo�e to by� ich odleg�o�� wektor�w, suma warto�ci bezwzgl�dnych ich r�nic,  lub wynik ich iloczynu skalarnego. Wsp�rz�dne pary punkt�w, odpowiadaj�cych parze najbardziej podobnych do siebie opis�w/wektor�w, maj� by� umieszczona w li�cie wynikowej ��cznie z miar� podobie�stwa. Funkcja powinna zwr�ci� list� N najbardziej podobnych opis�w. W tym celu mo�na np. list�  posortowa� (np. funkcja np.argsort ) i wzi�� jej pierwszych N element�w (mo�na te� zrobi� to 'r�cznie' przez N-krotne wybieranie najbardziej podobnego dopasowania).

2.4.Wczytaj obrazy fontanna1.jpg  i fontanna2.jpg. Znajd� dla nich punkty charakterystyczne metod� Harrisa za pomoc� funkcji z poprzednich zaj��. Dla znalezionych punkt�w stw�rz listy opis�w za pomoc� funkcji z punktu 2.2. Rozmiar otoczenia ustaw 15 (mo�esz poeksperymentowa� z innymi ustawieniami). Wyszukaj najlepsze dopasowania za pomoc� funkcji z punktu 2.3. Parametr N mo�na ustawi� na 20,

2.5. Pora na wy�wietlenie rezultat�w. W�r�d danych do �wiczenia znajduje si� plik pm.py  Mo�na zaimportowa� go do swojego pliku (import pm) i wykorzysta� znajduj�c� si� w nim funkcj� pm.plot_matches. Jednak�e mo�e by� konieczne dostosowanie tej funkcji do Pa�stwa listy zwr�conej przez funkcj� z p.2.3. (dostarczona implementacja zak�ada, �e ka�da para jest zapisana w postaci ([y1, x1], [y2,x2]) ).

2.6. Powt�rz operacje z punkt�w 2.4 i 2.5 dla obraz�w 'budynek1.jpg' i 'budynek2.jpg'. Zauwa�, �e na tych obrazach budynki s� po�o�one pod nieco innym k�tem. Czy wp�yn�o to na jako�� dopasowania?

2.7. Powt�rz operacje z punkt�w 2.4 i 2.5 dla obraz�w 'fontanna1.jpg' i 'fontanna_pow.jpg'. Obrazy znaczne r�ni� si� skal�. Czy Harris poradzi� sobie z tak� r�nic�?

2.8. Powt�rz operacje z punkt�w 2.4 i 2.5 dla obraz�w 'eiffel1.jpg' i 'eiffel2.jpg'. Obrazy r�ni� si� jasno�ci� i nieco skal�. Czy Harris poradzi� sobie z tak� r�nic�?

2.9. Zmodyfikuj funkcj� wyznaczaj�c� opisy punkt�w (z p.2.2), tak aby uwzgl�dni� afiniczne zmiany jasno�ci:

w = w - w�r |w - w�r| 

Przy czym �redni� mo�na wyznaczy� jako np.mean(w) a:

|w - w�r|
jako odchylenie standardowe za pomoc� np.std(w).

Spr�buj powt�rzy� operacje z p.2.8 dla tak zmodyfikowanych opis�w. Czy nast�pi�a jaka� poprawa?

3. SIFT
3.1. Wykorzystuj�c implementacj� metody SIFT z opencv przeprowad� operacje analogiczne do tych z punktu 2 (znalezienie podobnych do siebie otocze� punkt�w charakterystycznych). W tym celu wywo�aj funkcj�  cv2.xfeatures2d.SIFT_create() kt�ra tworzy obiekt realizuj�cy r�ne operacje na obrazach z wykorzystaniem metody SIFT. Nast�pnie u�yj dwukrotnie metody detectAndCompute tego obiektu dla dw�ch obraz�w: fontanna1.jpg  i fontanna2.jpg.  Parametrami tej metody powinny by� obraz w odcieniach jasno�ci i None. Metoda zwraca dwie listy - list� punkt�w charakterystycznych i list� ich opis�w (deskrypcji). Do por�wnania opis�w u�yj 'por�wnywarki'  z opencv - BFMatcher i metody k najbli�szych s�siad�w (k=2, gdy� interesuje nas najbardziej podobne otoczenie oraz nast�pne wg. podobie�stwa - b�dzie to wykorzystane przy rysowaniu wynik�w). Przyk�adowo, dla list opis�w des1 i des2 list� pasuj�cych do siebie punkt�w matches uzyskuje si� nast�puj�cao:

   bf = cv2.BFMatcher()

   matches = bf.knnMatch(des1,des2, k=2)
    

Tak uzyskan� list� dopasowa� mo�na wy�wietli� jako obraz zwracany prze funkcj� cv2.drawMatchesKnn wywo�an� z nast�puj�cymi parametrami: pierwszy obraz, punkty charakterystyczne pierwszego obrazu, drugi obraz, punkty charakterystyczne drugiego obrazu, lista dopasowanych punkt�w (z knnMatch), obraz wyj�ciowy (ustawiamy na None, obraz wyj�ciowy jest tak�e zwracany przez t� funkcj�), flags=2 (bez tego argumentu wy�wietlone zostan� wszystkie punkty charakterystyczne).

UWAGA - aby pozostawi� tylko najlepsze dopasowania mo�na z listy matches przed zawo�aniem drawMatchesKnn usun�� te, kt�rych drugi s�siad (z knn)  ma  do�� podobne otoczenie. Realizuje to przyk�adowa p�tla:

    best_matches = [ ]
    for m,n in matches: # m i n - najlepsze i 'drugie najlepsze' dopasowanie
        if m.distance < 0.75*n.distance:  # najlepsze jest lepsze ni� 3/4 'drugiego'
            best_matches.append([m])

  

3.2. Pon�w operacje z p.3.1 dla obraz�w przetwarzanych w punktach od 2.6 do 2.9. Jak SIFT radzi sobie w por�wnaniu z opisem bazuj�cym na wycinkach?