Uog�lniona transformata Hougha
1. Cel zaj��
implementacja uog�lnionej transformaty Hougha
wyszukiwanie wzorc�w za pomoc�  uog�lnionej transformaty Hougha
2. Implementacja uog�lnionej transformaty Hougha
2.1.Ze strony kursu pobierz archiwum z danymi do �wiczenia i rozpakuj je we w�asnym katalogu roboczym.

2.2. Utw�rz nowy skrypt. No podstawie obrazu ze wzorcem 'trybik.jpg' stw�rz tablic� R-table. W tym celu wyznacz kontury oraz gradienty na obrazie wzorca. Kontury mo�na wyznaczy� podobnie jak w �wiczeniu z odleg�o�ci Hausdorffa, natomiast do wyliczenia gradient�w mo�na wykorzysta� filtry Sobela, przyk�adowo:

sobelx = cv2.Sobel(im,cv2.CV_64F,1,0,ksize=5)

sobely = cv2.Sobel(im,cv2.CV_64F,0,1,ksize=5)

Nale�y wyliczy� 2 macierze (obrazy) - zar�wno warto�� gradientu (pierwiastek sumy kwadrat�w Sobela pionowego i poziomego) jak i orientacj� (wykorzystuj�c funkcj� np.arctan2). Macierz warto�ci gradientu warto znormalizowa� dziel�c j� przez jej warto�� maksymaln�.

Przed wype�nieniem R-table nale�y wybra� punkt referencyjny - niech b�dzie to �rodek ci�ko�ci wzorca wyznaczany ze zbinaryzowanego obrazu wzorca z wykorzystaniem moment�w (jak w �wiczeniu z odleg�o�ci Hausdorffa).

Do wype�nienie R-table b�d� potrzebne wektory ��cz�ce  punkty konturu/kontur�w (we wzorcu mog� wyst�pi� 'dziury') z punktem referencyjnum. Do R-table wpisujemy d�ugo�ci tych wektor�w oraz k�ty jaki tworz� z osi� OX (tu zn�w przyda si� funkcja  np.arctan2). Miejsce wpisania do tablicy R-table wyznacza orientacja gradientu w punkcie konturu, przy czym prosz� przeliczy� radiany na stopnie - R-table bedzie mia�a 360 wierszy.. R-table mozna zaimplementowa� jako lista 360 list:

Rtable =  [[] for i in range(360)]. W�wczas np Rtable[30] b�dzie list� wsp�rz�dnych biegunowych punkt�w konturu, gt�rych gradient orientacji wynosi 30o

2.3. Na podstawie obrazu 'trybiki2.jpg' oraz R-table z poprzedniego punktu wype�nij dwuwymiarow� przestrze� Hougha - wylicz gradient w ka�dym punkcie jak w punkcie 2.2 i dla punkt�w, kt�rych znormalizowana warto�� gradientu przekracza 0.5 dodaj jeden w przestrzeni akumulacyjnej w punktach wynikaj�cych z wpis�w do R-table - czyli w punktach:

x1 = r*np.cos(fi) + x 
y1 = r*np.sin(fi) + y, gdzie r,fi - warto�ci z R-table, natomiast x,y - wsp�rz�dne punktu przekraczaj�cego 0,5,

2.4. Wyszukaj maksimum w przestrzeni Hougha i zaznacz je w obrazie wej�ciowym (na przyk�ad z wykorzystaniem znanej funkcji: plt.plot([mx[1]], [mx[0]],'*', color='r'))

2.5. Poka� wyniki prowadz�cemu

3. Wyszukiwanie wzorc�w r�ni�cych si� orientacj�
3.1 Teraz zwi�kszymy przestrze� Hougha do 3 wymiar�w dodaj�c obroty. Przeszta�� kod z punktu 2.3 tak, aby dodawanie jedynki by�o powt�rzone dla co dziesi�tego k�ta z zakresu [0-360) (k�ty odejmujemy od fi). Powi�kszenie przestrzeni Hougha o trzeci wymiar mozna zrealizowa� przez powi�kszenie 'shape' jak poni�ej;

new_hough_shape = hough.shape + (36,)

new_hough=np.zeros(new_hough_shape);

(36,) jest tu jednoelementow� krotk� - reprezentuje ona trzeci wymiar - co dziesi�ty stopie� k�ta

3.2 W celu wykrycia wszystkich wzorc�w na obrazie nale�a�oby wykry� odpowiednio du�e maksima lokalne. Jednak�e dla u�atwienia zast�pimy t� operacj� kilkukrotnym wykrywaniem maksimum globalnego i wyzerowaniem jego otoczenia. Do znalezienia maksimum w 3-wymiarowej przestrzeni Hougha mo�na wykorzysta� metod� tablicy numpy  - argmax(). Jednak�e zwraca ona jeden indeks w tablicy 'sp�aszczonej' do jednego wymiaru. Do uzyskania u�ytecznych dla nas indeks�w (po 3 wymiarach) nale�y wynik argmax() poda� do funkcji np.unravel_index (wraz z 'shapem' tablicy). Po znalezieniu maksimum zaznacz je w obrazie wej�ciowym (potrzebne s� tylko 2 wsp�rz�dne maksimum, k�t na razie nie jest istotny).

3.3 Je�eli znalezione zosta�o to samo maksimum co w punkcie 2.4 (a k�t wynosi 0) wyzeruj otoczenie maksimum w przestrzeni Hougha - przyk�adowo:

hough[m[0]-delta:m[0]+delta, m[1]-delta:m[1]+delta, :] = 0, gdzie m zawiera indeksy maksimum, a delta to rozmiar otoczenia (mo�e przyj�� warto�� 30) 
Nast�pnie pon�w operacje z punktu 3.2. Wyszukaj i zaznacz w sumie 5 kolejnych maksim�w. Sprawd� czy znalezione zosta�y wzorce.

3.4 Dodatkowo mo�na dla �adniejszej wizualizacji wyrysowa� wzorzec w znalezionych punktach. W tym celu nale�y wyrysowa� w obrazie wej�ciowym punkty odpowiadaj�ce wszystkim wektorom z tablicy R-table u�ywaj�c wzor�w bardzo podobnych do tych z punktu 2.3 (z poprawk� z 3.1), przy czym x,y to b�d� wsp�rz�dne maksimum, a poprawka z punktu 3.1 b�dzie dotyczy� orientacji maksimum (dodatkowo nale�y tu uzwgl�dni� zmian� zwrotu wektor�w wpisanych do R-table - czyli doda� ? )

3.5. Poka� wyniki prowadz�cemu