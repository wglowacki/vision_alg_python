Uogólniona transformata Hougha
1. Cel zajêæ
implementacja uogólnionej transformaty Hougha
wyszukiwanie wzorców za pomoc¹  uogólnionej transformaty Hougha
2. Implementacja uogólnionej transformaty Hougha
2.1.Ze strony kursu pobierz archiwum z danymi do æwiczenia i rozpakuj je we w³asnym katalogu roboczym.

2.2. Utwórz nowy skrypt. No podstawie obrazu ze wzorcem 'trybik.jpg' stwórz tablicê R-table. W tym celu wyznacz kontury oraz gradienty na obrazie wzorca. Kontury mo¿na wyznaczyæ podobnie jak w æwiczeniu z odleg³oœci Hausdorffa, natomiast do wyliczenia gradientów mo¿na wykorzystaæ filtry Sobela, przyk³adowo:

sobelx = cv2.Sobel(im,cv2.CV_64F,1,0,ksize=5)

sobely = cv2.Sobel(im,cv2.CV_64F,0,1,ksize=5)

Nale¿y wyliczyæ 2 macierze (obrazy) - zarówno wartoœæ gradientu (pierwiastek sumy kwadratów Sobela pionowego i poziomego) jak i orientacjê (wykorzystuj¹c funkcjê np.arctan2). Macierz wartoœci gradientu warto znormalizowaæ dziel¹c j¹ przez jej wartoœæ maksymaln¹.

Przed wype³nieniem R-table nale¿y wybraæ punkt referencyjny - niech bêdzie to œrodek ciê¿koœci wzorca wyznaczany ze zbinaryzowanego obrazu wzorca z wykorzystaniem momentów (jak w æwiczeniu z odleg³oœci Hausdorffa).

Do wype³nienie R-table bêd¹ potrzebne wektory ³¹cz¹ce  punkty konturu/konturów (we wzorcu mog¹ wyst¹piæ 'dziury') z punktem referencyjnum. Do R-table wpisujemy d³ugoœci tych wektorów oraz k¹ty jaki tworz¹ z osi¹ OX (tu znów przyda siê funkcja  np.arctan2). Miejsce wpisania do tablicy R-table wyznacza orientacja gradientu w punkcie konturu, przy czym proszê przeliczyæ radiany na stopnie - R-table bedzie mia³a 360 wierszy.. R-table mozna zaimplementowaæ jako lista 360 list:

Rtable =  [[] for i in range(360)]. Wówczas np Rtable[30] bêdzie list¹ wspó³rzêdnych biegunowych punktów konturu, gtórych gradient orientacji wynosi 30o

2.3. Na podstawie obrazu 'trybiki2.jpg' oraz R-table z poprzedniego punktu wype³nij dwuwymiarow¹ przestrzeñ Hougha - wylicz gradient w ka¿dym punkcie jak w punkcie 2.2 i dla punktów, których znormalizowana wartoœæ gradientu przekracza 0.5 dodaj jeden w przestrzeni akumulacyjnej w punktach wynikaj¹cych z wpisów do R-table - czyli w punktach:

x1 = r*np.cos(fi) + x 
y1 = r*np.sin(fi) + y, gdzie r,fi - wartoœci z R-table, natomiast x,y - wspó³rzêdne punktu przekraczaj¹cego 0,5,

2.4. Wyszukaj maksimum w przestrzeni Hougha i zaznacz je w obrazie wejœciowym (na przyk³ad z wykorzystaniem znanej funkcji: plt.plot([mx[1]], [mx[0]],'*', color='r'))

2.5. Poka¿ wyniki prowadz¹cemu

3. Wyszukiwanie wzorców ró¿ni¹cych siê orientacj¹
3.1 Teraz zwiêkszymy przestrzeñ Hougha do 3 wymiarów dodaj¹c obroty. Przeszta³æ kod z punktu 2.3 tak, aby dodawanie jedynki by³o powtórzone dla co dziesi¹tego k¹ta z zakresu [0-360) (k¹ty odejmujemy od fi). Powiêkszenie przestrzeni Hougha o trzeci wymiar mozna zrealizowaæ przez powiêkszenie 'shape' jak poni¿ej;

new_hough_shape = hough.shape + (36,)

new_hough=np.zeros(new_hough_shape);

(36,) jest tu jednoelementow¹ krotk¹ - reprezentuje ona trzeci wymiar - co dziesi¹ty stopieñ k¹ta

3.2 W celu wykrycia wszystkich wzorców na obrazie nale¿a³oby wykryæ odpowiednio du¿e maksima lokalne. Jednak¿e dla u³atwienia zast¹pimy tê operacjê kilkukrotnym wykrywaniem maksimum globalnego i wyzerowaniem jego otoczenia. Do znalezienia maksimum w 3-wymiarowej przestrzeni Hougha mo¿na wykorzystaæ metodê tablicy numpy  - argmax(). Jednak¿e zwraca ona jeden indeks w tablicy 'sp³aszczonej' do jednego wymiaru. Do uzyskania u¿ytecznych dla nas indeksów (po 3 wymiarach) nale¿y wynik argmax() podaæ do funkcji np.unravel_index (wraz z 'shapem' tablicy). Po znalezieniu maksimum zaznacz je w obrazie wejœciowym (potrzebne s¹ tylko 2 wspó³rzêdne maksimum, k¹t na razie nie jest istotny).

3.3 Je¿eli znalezione zosta³o to samo maksimum co w punkcie 2.4 (a k¹t wynosi 0) wyzeruj otoczenie maksimum w przestrzeni Hougha - przyk³adowo:

hough[m[0]-delta:m[0]+delta, m[1]-delta:m[1]+delta, :] = 0, gdzie m zawiera indeksy maksimum, a delta to rozmiar otoczenia (mo¿e przyj¹æ wartoœæ 30) 
Nastêpnie ponów operacje z punktu 3.2. Wyszukaj i zaznacz w sumie 5 kolejnych maksimów. SprawdŸ czy znalezione zosta³y wzorce.

3.4 Dodatkowo mo¿na dla ³adniejszej wizualizacji wyrysowaæ wzorzec w znalezionych punktach. W tym celu nale¿y wyrysowaæ w obrazie wejœciowym punkty odpowiadaj¹ce wszystkim wektorom z tablicy R-table u¿ywaj¹c wzorów bardzo podobnych do tych z punktu 2.3 (z poprawk¹ z 3.1), przy czym x,y to bêd¹ wspó³rzêdne maksimum, a poprawka z punktu 3.1 bêdzie dotyczyæ orientacji maksimum (dodatkowo nale¿y tu uzwglêdniæ zmianê zwrotu wektorów wpisanych do R-table - czyli dodaæ ? )

3.5. Poka¿ wyniki prowadz¹cemu