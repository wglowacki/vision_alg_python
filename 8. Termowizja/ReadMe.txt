Termowizja
Prosta analiza obrazu termowizyjnego
Obraz termowizyjne maj� t� zalet�, �e obiekty np. ludzie s� na nich zwykle do�� dobrze widoczni (tj. wyr�niaj� si� od t�a). Wyj�tkiem jest sytuacja, gdy temperatura t�a jest zbli�ona do temperatury obiektu - w bardzo ciep�y dzie�.

W pierwszym etapie do detekcji sylwetek ludzi wykorzystamy nast�puj�ce algorytmy:

- binaryzacja

- filtracja

- indeksacja

- analiza wynik�w indeksacji,

1. Ze strony kursu pobierz sekwencj� vid1_IR.avi.

2. Wczytywanie sekwencji w OpenCV jest wzgl�dnie proste:

cap = cv2.VideoCapture('vid1_IR.avi')

while(cap.isOpened()):

ret, frame = cap.read()

G = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imshow('IR',G)

if cv2.waitKey(1) & 0xFF == ord('q'):

break

cap.release()

Uwaga. Zamiast nazwy pliku mo�na poda� liczb� (np. 0) � wtedy aplikacja spr�buje si� po��czy� z kamer� (USB, wbudowan�), oczywi�cie o ile taka jest dost�pna w systemie. Mo�na te� poda� adres kamery IP dzia�aj�cej w protokole rtsp.

3. Binaryzacja � w pierwszym przybli�eniu prosz� zastosowa� sta�y pr�g. Dla przypomnienia: cv2.threshold (szczeg�y sprawdzi� w dokumentacji). Warto�� progu nale�y dobra� eksperymentalnie, tak aby sylwetki by� jak najlepiej wyodr�bnione, przy jednoczesnym braku szum�w. Od razu nale�y zaznaczy�, �e nie da si� tego zrobi� idealnie.

4. Filtracja � mo�na wykorzysta� ca�y ,,arsena�'' �rodk�w � filtry medianowe oraz operacje morfologiczne.

5. Indeksacja � funkcje connectedComponents oraz connectedComponentsWithStats. Sugeruje si� u�ycie drugiej wersji (obliczane s� od razu pole, prostok�t otaczaj�cy oraz �rodek ci�ko�ci). Spos�b dost�pu wynik�w prosz� odszuka� w dokumentacji.

6. Analiza wynik�w indeksacji:

a) w pierwszym kroku proponuje si� wy�wietlenie prostok�t�w otaczaj�cych dla wszystkich obiekt�w � funkcja cv2.rectangle

b) najprostsze kryterium to rozmiar � obiekty powinny by� wi�ksze ni� X (dobra�).

c) mo�na te� analizowa� kszta�ty � szukamy pionowych sylwetek.

d) ostatni i najtrudniejszy element, to pr�ba po��czenia sylwetek, kt�re s� podzielone. Jest to cz�sto wyst�puj�ce zjawisko na obrazach termowizyjnych os�b ubranych (ciep�o, grubo). Ods�oni�te cz�ci cia�a, takie jak g�owa, r�ce s� najja�niejsze, a okolice pasa i n�g najciemniejsze. W tym przypadku warto rozwa�y� heurystyk�, polegaj�c� na sklejaniu le��cych ,,jeden pod drugim'' prostok�t�w otaczaj�cych � do samodzielnego zaprojektowania.

Detekcja obiekt�w z wykorzystaniem wzorca probabilistycznego.
Inne podej�cie do zagadnienia detekcji pieszych polega na obserwacji, �e sylwetki stoj�cych os�b maj� do�� charakterystyczny i powtarzalny wygl�d. Pozawala to na stworzenie ,,wzorca'' sylwetki, a nast�pie wyszukiwanie go na obrazie (technika okna przesuwnego).

W pierwszym etapie potrzebna b�dzie baza wycink�w sylwetek o okre�lonych rozmiarach � 192 x XX. W celu ich pozyskania wykorzystamy aplikacj� z cz�ci pierwszej � dodajmy do niej zapisywanie do pliku png zweryfikowanych sylwetek.

1. Wyci�cie ROI - roi = gray[y1:y2, x1:x2]

2. Zapis ROI - cv2.imwrite('sample_%06d.png' % iPedestrian,ROI)

iPedestrian to licznik globalny � nale�y inkrementowa� co zapis,

3. Wybieramy ok. 30 -50 zdj��. Zasadniczo powinny one by� frontalne, ale dopuszcza si� r�wnie� zrobione z boku.

4. W kolejnym kroku, w osobnym skrypcie nale�y zdj�cia wczyta�, przeskalowa� i wyznaczy� wzorzec. Aby sobie u�atwi� �ycie, mo�na dla wybranych pr�bek zmieni� nazw� (na kolejne liczby). Przyk�adowo w programie DoubleCommander dost�pne jest MultiRename tool. Inna opcja to np. taka sk�adania:

from os import listdir

from os.path import isfile, join

onlyfiles = [f for f in listdir('samples') if isfile(join('samples', f))]

Skalowanie cv2.resize � do rozmiaru 192 x 64

Binaryzacja (jak wcze�niej, cho� mo�na rozwa�y� zmian� progu). Uwaga. Nale�y zmieni� przypisywan� warto�� wyj�ciow� z 255 na 1.

W razie potrzeby, mo�na rozwa�y� te� filtracj�.

Ostatecznie wzorzec probabilistyczny powstaje na zasadzie DPM = DPM + B, przy czym B musi by� binarny, a nie [0;1].

Otrzymany wzorzec zapisujemy do pliku.

Do samej detekcji wykorzystujemy trzeci skrypt.

W nim realizujemy wczytywanie sekwencji podobne jak w pierwszym, przy czym w pierwszym etapie najlepiej prze�wiczy� dzia�ania metody na wybranej ramce. Przyk�adowo na stronie kursu, inne mo�na pozyska� zapisuj�c ramki do png w programie 1.

Wczytujemy te� wzorzec (potrzeba konwersja do odcieni szaro�ci). Konwertujemy do typu float32, dzielimy przez liczb� obraz�w, z kt�rych zosta� utworzony (skalowanie do zakresu 0-1, wynik oznaczamy DMP_1) oraz obliczamy negacj� DPM_0 = (1-DPM) tj. prawdopodobie�stwo przynale�no�ci do t�a.

Binaryzujemy obraz z sekwencji testowej. Nast�pnie prowadzimy analiz� w oknie 192 x 64 (technika okna przesuwnego). Przyk�adamy takie okno to kolejnych lokalizacji na obrazie (mo�na rozwa�y� krok wi�kszy ni� 1). Dla maski binarnej (B) zliczamy prawdopodobie�stwo, �e jest sylwetk� ludzk�:

sum_x sum_y B(x,y)*DPM_1(x,y)+(1-B(x,y))*DPM_0(x,y).

Wynik zapisujemy w obrazie pomocniczym: result = np.zeros((360,480), np.float32)

Do wizualizacji nale�y wyniki znormalizowa�:

result = result / np.max(np.max(result))

ruint8 = np.uint8(result*255)

Ostatni etap to odnajdywanie maksim�w lokalnych.

Najprostsze rozwi�zanie to szukanie maksimum �na bie��co�, podczas analizy poszczeg�lnych okien. Przy czym to podej�cie pozwala znale�� tylko jedno maksimum. Prosz� sprawdzi� i narysowa� prostok�t otaczaj�cy dla znalezionej postaci.

W ramach pracy w�asnej prosz� opracowa� metod� znajdywania wielu maksim�w. Nale�y przy tym pami�ta� o dw�ch sprawach: a) ustali� pr�g dolny, b) zastosowa� eliminacj� obszar�w ju� odwiedzonych.