1. Cel zajêæ
zapoznanie z zagadnieniem opisywania punktów charakterystycznych
otoczenie punktu jako deskryptor
porównanie dzia³ania metody Harrisa i SIFT
2. Prosta deskrypcja punktów charakterystycznych
2.1. UWAGA - niniejsze æwiczenie jest kontynuacj¹ poprzedniego - bêd¹ w nim potrzebne zarówno obrazy jak i funkcje z poprzedniego æwiczenia. Ze strony kursu pobierz archiwum z dodatkowymi danymi do æwiczenia i rozpakuj je we w³asnym katalogu roboczym.

2.2. W skrypcie z ubieg³ego tygodnia dodaj funkcjê tworz¹c¹ opisy punktów charakterystycznych (w postaci ich otoczeñ). Jako parametry funkcja powinna otrzymaæ obraz, listê wspó³rzêdnych punktów charakterystycznych (wynik funkcji z poprzednich zajêæ) oraz wielkoœæ otoczenia.Z listy punktów nale¿y usun¹æ wszystkie punkty, których otoczenia nie mieszcz¹ siê w obrazie.

Dygresja - mo¿na wykorzystaæ funkcjê filter z anonimow¹ funkcj¹ lambda yx:  yx[0]>=s and yx[0]<Y-s and yx[1]>=s and yx[1]<X-s - przyk³adowo:

lista=list(filter(lambda yx:  yx[0]>=s and yx[0]<Y-s and yx[1]>=s and yx[1]<X-s, lista))   

Nastêpnie nale¿y  stworzyæ listê opisów punktów po odfiltrowaniu. Opisem bêdzie wycinek obrazu z otoczenia punktu o rozmiarze podanym przez parametr. Przy czym dobrze bêdzie sprowadziæ go do wektora. Je¿eli np. p jest wycinkiem, to za pomoc¹ p.flatten( ) uzyskuje siê z niego wektor. Jako wynik funkcji nale¿y zwróciæ listê otoczeñ uzupe³nionych o wspó³rzêdne ich punktów centralnych.

Dygresja - w tym celu mo¿na zzipowaæ przefiltrowan¹ listê wspó³rzêdnych z list¹ otoczeñ (funkcja zip) - przyk³adowo 

wynik = list(zip(l_otoczen, l_wspolrzednych)) i zwracamy wynik

2.3. Dodaj funkcjê porównuj¹c¹ opisy punktów charaktereystycznych z dwóch obrazów i znajduj¹c¹ opisy najbardziej podobne. Funkcja jako parametry powinna otrzymaæ dwie listy opisów punktów charakterystycznych (z funkcji z p.2.2) oraz liczbê N najbardziej podobnych do siebie opisów. Funkcja mo¿e wykorzystaæ metodê 'ka¿dy z ka¿dym' - ka¿dy opis punktu z listy pierwszej jest porównywany ze wszystkimi opisami z listy drugiej i wybierany jest opis najbardziej podobny. Mo¿na ró¿nie okreœliæ miarê podobieñstwa.  Mo¿e to byæ ich odleg³oœæ wektorów, suma wartoœci bezwzglêdnych ich ró¿nic,  lub wynik ich iloczynu skalarnego. Wspó³rzêdne pary punktów, odpowiadaj¹cych parze najbardziej podobnych do siebie opisów/wektorów, maj¹ byæ umieszczona w liœcie wynikowej ³¹cznie z miar¹ podobieñstwa. Funkcja powinna zwróciæ listê N najbardziej podobnych opisów. W tym celu mo¿na np. listê  posortowaæ (np. funkcja np.argsort ) i wzi¹æ jej pierwszych N elementów (mo¿na te¿ zrobiæ to 'rêcznie' przez N-krotne wybieranie najbardziej podobnego dopasowania).

2.4.Wczytaj obrazy fontanna1.jpg  i fontanna2.jpg. ZnajdŸ dla nich punkty charakterystyczne metod¹ Harrisa za pomoc¹ funkcji z poprzednich zajêæ. Dla znalezionych punktów stwórz listy opisów za pomoc¹ funkcji z punktu 2.2. Rozmiar otoczenia ustaw 15 (mo¿esz poeksperymentowaæ z innymi ustawieniami). Wyszukaj najlepsze dopasowania za pomoc¹ funkcji z punktu 2.3. Parametr N mo¿na ustawiæ na 20,

2.5. Pora na wyœwietlenie rezultatów. Wœród danych do æwiczenia znajduje siê plik pm.py  Mo¿na zaimportowaæ go do swojego pliku (import pm) i wykorzystaæ znajduj¹c¹ siê w nim funkcjê pm.plot_matches. Jednak¿e mo¿e byæ konieczne dostosowanie tej funkcji do Pañstwa listy zwróconej przez funkcjê z p.2.3. (dostarczona implementacja zak³ada, ¿e ka¿da para jest zapisana w postaci ([y1, x1], [y2,x2]) ).

2.6. Powtórz operacje z punktów 2.4 i 2.5 dla obrazów 'budynek1.jpg' i 'budynek2.jpg'. Zauwa¿, ¿e na tych obrazach budynki s¹ po³o¿one pod nieco innym k¹tem. Czy wp³ynê³o to na jakoœæ dopasowania?

2.7. Powtórz operacje z punktów 2.4 i 2.5 dla obrazów 'fontanna1.jpg' i 'fontanna_pow.jpg'. Obrazy znaczne ró¿ni¹ siê skal¹. Czy Harris poradzi³ sobie z tak¹ ró¿nic¹?

2.8. Powtórz operacje z punktów 2.4 i 2.5 dla obrazów 'eiffel1.jpg' i 'eiffel2.jpg'. Obrazy ró¿ni¹ siê jasnoœci¹ i nieco skal¹. Czy Harris poradzi³ sobie z tak¹ ró¿nic¹?

2.9. Zmodyfikuj funkcjê wyznaczaj¹c¹ opisy punktów (z p.2.2), tak aby uwzglêdniæ afiniczne zmiany jasnoœci:

w = w - wœr |w - wœr| 

Przy czym œredni¹ mo¿na wyznaczyæ jako np.mean(w) a:

|w - wœr|
jako odchylenie standardowe za pomoc¹ np.std(w).

Spróbuj powtórzyæ operacje z p.2.8 dla tak zmodyfikowanych opisów. Czy nast¹pi³a jakaœ poprawa?

3. SIFT
3.1. Wykorzystuj¹c implementacjê metody SIFT z opencv przeprowadŸ operacje analogiczne do tych z punktu 2 (znalezienie podobnych do siebie otoczeñ punktów charakterystycznych). W tym celu wywo³aj funkcjê  cv2.xfeatures2d.SIFT_create() która tworzy obiekt realizuj¹cy ró¿ne operacje na obrazach z wykorzystaniem metody SIFT. Nastêpnie u¿yj dwukrotnie metody detectAndCompute tego obiektu dla dwóch obrazów: fontanna1.jpg  i fontanna2.jpg.  Parametrami tej metody powinny byæ obraz w odcieniach jasnoœci i None. Metoda zwraca dwie listy - listê punktów charakterystycznych i listê ich opisów (deskrypcji). Do porównania opisów u¿yj 'porównywarki'  z opencv - BFMatcher i metody k najbli¿szych s¹siadów (k=2, gdy¿ interesuje nas najbardziej podobne otoczenie oraz nastêpne wg. podobieñstwa - bêdzie to wykorzystane przy rysowaniu wyników). Przyk³adowo, dla list opisów des1 i des2 listê pasuj¹cych do siebie punktów matches uzyskuje siê nastêpuj¹cao:

   bf = cv2.BFMatcher()

   matches = bf.knnMatch(des1,des2, k=2)
    

Tak uzyskan¹ listê dopasowañ mo¿na wyœwietliæ jako obraz zwracany prze funkcjê cv2.drawMatchesKnn wywo³an¹ z nastêpuj¹cymi parametrami: pierwszy obraz, punkty charakterystyczne pierwszego obrazu, drugi obraz, punkty charakterystyczne drugiego obrazu, lista dopasowanych punktów (z knnMatch), obraz wyjœciowy (ustawiamy na None, obraz wyjœciowy jest tak¿e zwracany przez tê funkcjê), flags=2 (bez tego argumentu wyœwietlone zostan¹ wszystkie punkty charakterystyczne).

UWAGA - aby pozostawiæ tylko najlepsze dopasowania mo¿na z listy matches przed zawo³aniem drawMatchesKnn usun¹æ te, których drugi s¹siad (z knn)  ma  doœæ podobne otoczenie. Realizuje to przyk³adowa pêtla:

    best_matches = [ ]
    for m,n in matches: # m i n - najlepsze i 'drugie najlepsze' dopasowanie
        if m.distance < 0.75*n.distance:  # najlepsze jest lepsze ni¿ 3/4 'drugiego'
            best_matches.append([m])

  

3.2. Ponów operacje z p.3.1 dla obrazów przetwarzanych w punktach od 2.6 do 2.9. Jak SIFT radzi sobie w porównaniu z opisem bazuj¹cym na wycinkach?