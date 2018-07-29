Termowizja
Prosta analiza obrazu termowizyjnego
Obraz termowizyjne maj¹ t¹ zaletê, ¿e obiekty np. ludzie s¹ na nich zwykle doœæ dobrze widoczni (tj. wyró¿niaj¹ siê od t³a). Wyj¹tkiem jest sytuacja, gdy temperatura t³a jest zbli¿ona do temperatury obiektu - w bardzo ciep³y dzieñ.

W pierwszym etapie do detekcji sylwetek ludzi wykorzystamy nastêpuj¹ce algorytmy:

- binaryzacja

- filtracja

- indeksacja

- analiza wyników indeksacji,

1. Ze strony kursu pobierz sekwencjê vid1_IR.avi.

2. Wczytywanie sekwencji w OpenCV jest wzglêdnie proste:

cap = cv2.VideoCapture('vid1_IR.avi')

while(cap.isOpened()):

ret, frame = cap.read()

G = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imshow('IR',G)

if cv2.waitKey(1) & 0xFF == ord('q'):

break

cap.release()

Uwaga. Zamiast nazwy pliku mo¿na podaæ liczbê (np. 0) – wtedy aplikacja spróbuje siê po³¹czyæ z kamer¹ (USB, wbudowan¹), oczywiœcie o ile taka jest dostêpna w systemie. Mo¿na te¿ podaæ adres kamery IP dzia³aj¹cej w protokole rtsp.

3. Binaryzacja – w pierwszym przybli¿eniu proszê zastosowaæ sta³y próg. Dla przypomnienia: cv2.threshold (szczegó³y sprawdziæ w dokumentacji). Wartoœæ progu nale¿y dobraæ eksperymentalnie, tak aby sylwetki by³ jak najlepiej wyodrêbnione, przy jednoczesnym braku szumów. Od razu nale¿y zaznaczyæ, ¿e nie da siê tego zrobiæ idealnie.

4. Filtracja – mo¿na wykorzystaæ ca³y ,,arsena³'' œrodków – filtry medianowe oraz operacje morfologiczne.

5. Indeksacja – funkcje connectedComponents oraz connectedComponentsWithStats. Sugeruje siê u¿ycie drugiej wersji (obliczane s¹ od razu pole, prostok¹t otaczaj¹cy oraz œrodek ciê¿koœci). Sposób dostêpu wyników proszê odszukaæ w dokumentacji.

6. Analiza wyników indeksacji:

a) w pierwszym kroku proponuje siê wyœwietlenie prostok¹tów otaczaj¹cych dla wszystkich obiektów – funkcja cv2.rectangle

b) najprostsze kryterium to rozmiar – obiekty powinny byæ wiêksze ni¿ X (dobraæ).

c) mo¿na te¿ analizowaæ kszta³ty – szukamy pionowych sylwetek.

d) ostatni i najtrudniejszy element, to próba po³¹czenia sylwetek, które s¹ podzielone. Jest to czêsto wystêpuj¹ce zjawisko na obrazach termowizyjnych osób ubranych (ciep³o, grubo). Ods³oniête czêœci cia³a, takie jak g³owa, rêce s¹ najjaœniejsze, a okolice pasa i nóg najciemniejsze. W tym przypadku warto rozwa¿yæ heurystykê, polegaj¹c¹ na sklejaniu le¿¹cych ,,jeden pod drugim'' prostok¹tów otaczaj¹cych – do samodzielnego zaprojektowania.

Detekcja obiektów z wykorzystaniem wzorca probabilistycznego.
Inne podejœcie do zagadnienia detekcji pieszych polega na obserwacji, ¿e sylwetki stoj¹cych osób maj¹ doœæ charakterystyczny i powtarzalny wygl¹d. Pozawala to na stworzenie ,,wzorca'' sylwetki, a nastêpie wyszukiwanie go na obrazie (technika okna przesuwnego).

W pierwszym etapie potrzebna bêdzie baza wycinków sylwetek o okreœlonych rozmiarach – 192 x XX. W celu ich pozyskania wykorzystamy aplikacjê z czêœci pierwszej – dodajmy do niej zapisywanie do pliku png zweryfikowanych sylwetek.

1. Wyciêcie ROI - roi = gray[y1:y2, x1:x2]

2. Zapis ROI - cv2.imwrite('sample_%06d.png' % iPedestrian,ROI)

iPedestrian to licznik globalny – nale¿y inkrementowaæ co zapis,

3. Wybieramy ok. 30 -50 zdjêæ. Zasadniczo powinny one byæ frontalne, ale dopuszcza siê równie¿ zrobione z boku.

4. W kolejnym kroku, w osobnym skrypcie nale¿y zdjêcia wczytaæ, przeskalowaæ i wyznaczyæ wzorzec. Aby sobie u³atwiæ ¿ycie, mo¿na dla wybranych próbek zmieniæ nazwê (na kolejne liczby). Przyk³adowo w programie DoubleCommander dostêpne jest MultiRename tool. Inna opcja to np. taka sk³adania:

from os import listdir

from os.path import isfile, join

onlyfiles = [f for f in listdir('samples') if isfile(join('samples', f))]

Skalowanie cv2.resize – do rozmiaru 192 x 64

Binaryzacja (jak wczeœniej, choæ mo¿na rozwa¿yæ zmianê progu). Uwaga. Nale¿y zmieniæ przypisywan¹ wartoœæ wyjœciow¹ z 255 na 1.

W razie potrzeby, mo¿na rozwa¿yæ te¿ filtracjê.

Ostatecznie wzorzec probabilistyczny powstaje na zasadzie DPM = DPM + B, przy czym B musi byæ binarny, a nie [0;1].

Otrzymany wzorzec zapisujemy do pliku.

Do samej detekcji wykorzystujemy trzeci skrypt.

W nim realizujemy wczytywanie sekwencji podobne jak w pierwszym, przy czym w pierwszym etapie najlepiej przeæwiczyæ dzia³ania metody na wybranej ramce. Przyk³adowo na stronie kursu, inne mo¿na pozyskaæ zapisuj¹c ramki do png w programie 1.

Wczytujemy te¿ wzorzec (potrzeba konwersja do odcieni szaroœci). Konwertujemy do typu float32, dzielimy przez liczbê obrazów, z których zosta³ utworzony (skalowanie do zakresu 0-1, wynik oznaczamy DMP_1) oraz obliczamy negacjê DPM_0 = (1-DPM) tj. prawdopodobieñstwo przynale¿noœci do t³a.

Binaryzujemy obraz z sekwencji testowej. Nastêpnie prowadzimy analizê w oknie 192 x 64 (technika okna przesuwnego). Przyk³adamy takie okno to kolejnych lokalizacji na obrazie (mo¿na rozwa¿yæ krok wiêkszy ni¿ 1). Dla maski binarnej (B) zliczamy prawdopodobieñstwo, ¿e jest sylwetk¹ ludzk¹:

sum_x sum_y B(x,y)*DPM_1(x,y)+(1-B(x,y))*DPM_0(x,y).

Wynik zapisujemy w obrazie pomocniczym: result = np.zeros((360,480), np.float32)

Do wizualizacji nale¿y wyniki znormalizowaæ:

result = result / np.max(np.max(result))

ruint8 = np.uint8(result*255)

Ostatni etap to odnajdywanie maksimów lokalnych.

Najprostsze rozwi¹zanie to szukanie maksimum „na bie¿¹co”, podczas analizy poszczególnych okien. Przy czym to podejœcie pozwala znaleŸæ tylko jedno maksimum. Proszê sprawdziæ i narysowaæ prostok¹t otaczaj¹cy dla znalezionej postaci.

W ramach pracy w³asnej proszê opracowaæ metodê znajdywania wielu maksimów. Nale¿y przy tym pamiêtaæ o dwóch sprawach: a) ustaliæ próg dolny, b) zastosowaæ eliminacjê obszarów ju¿ odwiedzonych.