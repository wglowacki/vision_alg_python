Transformata Fouriera-Mellina
1. Cel zajêæ
wyszukiwanie wzorców za pomoc¹  transformaty Fouriera-Mellina
2. Wyszukiwanie wzorca za pomoc¹ korelacji
2.1.Ze strony kursu pobierz archiwum z danymi do æwiczenia i rozpakuj je we w³asnym katalogu roboczym. UWAGA - W dzisiejszym æwiczeniu do wyœwietlania obrazów lepiej jest u¿ywaæ funkcji imshow z modu³u pyplot, a nie cv2.

2.2. Utwórz nowy skrypt. Wyszukaj wzorzec zapisany w obrazie 'wzor.pgm' na przeszukiwanym obrazie 'domek_r0.pgm'. Oba obrazy wczytaj w  odcieniach szaroœci. Zacznij od uzupe³nienia obraz wzorca zerami do rozmiaru obrazu przeszukiwanego (funkcja np.zeros(shape)). Najlepiej zrobiæ to tak, aby œrodek wzorca znalaz³ siê w punkcie (0,0) - wówczas maksimum korelacji wska¿e po³o¿enie wzorca na obrazie przeszukiwanym (podpowiedŸ - mozna najpierw wzorzec umieœciæ tak, aby jego œrodek pokry³ siê ze œrodkiem obrazu, a nastêpnie wykonaæ fftshift). PrzeprowadŸ korelacjê obrazu przeszukiwanego i obrazu wzorca z zerami w dziedzinie czêstotliwoœci. Do wyliczenia transformaty Fouriera wykorzystaj funkcje fft2 i fftshift z modu³u numpy.fft, a do transformaty odwrotnej ifft2 i ifftshift (z tego samego modu³u). Wspó³rzêdne maksimum w obrazie modu³u transformaty odwrotnej mo¿na uzyskaæ np. przy u¿yciu instrukcji:

 y,x = np.unravel_index( np.argmax(modul_odwrotnej), modul_odwrotnej.shape)

Modu³ liczby zespolonej uzyskujemy za pomoc¹ funkcji np.abs.

SprawdŸ, czy maksimum wypada w miejscu wystêpowania wzorca na obrazie przeszukiwanym (raczej nie powinno).

2.3. Zmieñ korelacjê na korelacjê fazow¹. SprawdŸ, czy maksimum wypada w miejscu wystêpowania wzorca na obrazie przeszukiwanym (teraz powinno byæ dobrze).

2.4. Zwizualizuj przesuniêcie przrekszta³caj¹c obraz wzorca z zerami (przed fftshift)  za pomoc¹ funkcji realizuj¹cej przekszta³cenie afiniczne - cv2.warpAffine. Przyk³adowy kod:

macierz_translacji = np.float32([[1,0,dx],[0,1,dy]])  - gdzie dx, dy - wektor przesuniêcia
obraz_przesuniety = cv2.warpAffine(obraz_wzorca_z, macierz_translacji, (obraz_wzorca_z.shape[1], obraz_wzorca_z.shape[0]))

Wektor przesuniecia, o ile œrodek wzorca znajdowa³ siê w punkcie (0,0), to:

dx = x - size_x //2

dy = y - size_y//2 

2.5. Poka¿ wyniki prowadz¹cemu

3. Wyszukiwanie wzorca niezale¿nie od obrotu i skali
3.1 Wczytaj obraz przeszukiwany 'domek_r30.pgm' oraz obraz wzorca 'domek_r0_64.pgm'. Uzupe³nij zerami obraz wzorca tak jak w punkcie 2.

Zrealizuj obliczenia z poni¿szego schematu uwzglêdniaj¹c nastêpuj¹ce uwagi:



- Uzupe³nij zerami mniejszy obraz tak jak w punkcie 2 ale z uwzglêdnieniem okna Hanninga uzyskanym funkcj¹:

def hanning2D(n):
    h = np.hanning(n)
    return np.sqrt(np.outer(h,h))

Okno przemna¿amy przez obraz przed uzupe³nieniem go zerami. n to rozmiar obrazu w pionie lub poziomie (zak³adamy, ¿e s¹ takie same)

- Przed transformacj¹ log-polar przefiltruj obrazy filtrem górnoprzepustowym uzyskanym funkcj¹:

def highpassFilter(size):
    rows = np.cos(np.pi*np.matrix([-0.5 + x/(size[0]-1) for x in range(size[0])]))
    cols = np.cos(np.pi*np.matrix([-0.5 + x/(size[1]-1) for x in range(size[1])]))
    X = np.outer(rows,cols)
    return (1.0 - X) * (2.0 - X)

size to shape obrazu filtrowanego. Filtrujemy w dziedzinie czêstotliwoœci, a wiêc polega to na przemno¿eniu obrazów amplitud przez filtr.

- Transformatê log-polar mo¿na zrealizowaæ za pomoc¹ funkcji cv2.logPolar. Œrodek przekszta³cenia to œrodek obrazu, natomiast parametr M proszê ustawiæ na:   2*R/np.log(R) gdzie R to max. promieñ, czyli po³owa rozmiaru pionowego lub poziomego. Parametr flags to: cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS.

- Uzyskane w wyniku pierwszej korelacji fazowej wspó³rzêdne maksimum (wsp_kata, wsp_logr) przeliczamy na  skalowanie i stopnie wg wzorów:

skala = np.exp(1/M) ** wykl  -  gdzie M to parametr funkcji cv2.logPolar, a wykl wyliczamy jako:

    if wsp_logr > np_fimlp.shape[1]//2:
        wykl =rozmiar_wsp_logr - wsp_logr
    else:
        wykl = - wsp_logr

kat1  =  360 - A                             - gdzie    A =  (wsp_kata * 360.0 ) / rozmiar_wsp_kata

kat2  =  360 - A - 180

K¹ty s¹ dwa, gdy¿ ze wzglêdu na symetriê modu³u widma czêstotliwoœciowego wykrywane s¹ obroty tylko do 180 stopni. Dlatego w nastepnym kroku trzeba sprawdziæ oba k¹ty i wybraæ ten, który daje lepsz¹ korelacjê.

- Wyliczone k¹ty i skalê nale¿y u¿yæ w przekszta³ceniu afinicznym, podobnie jak w zadaniu 2. Tym razem macierz translacji bêdzie wygl¹da³a nastêpuj¹co:

macierz_translacji = cv2.getRotationMatrix2D((srodekTrans[0], srodekTrans[1]), kat, skala) gdzie srodekTrans to œrodek obrazu:
srodekTrans = [math.floor((obraz.shape[0] + 1) / 2), math.floor((obraz.shape[1] + 1 ) / 2)]


 - Przetransformowane obrazy nale¿y poddaæ transformacie Fouriera i  skorelowaæ z widmemem obrazu przeszukiwanego. Z wyniku daj¹cego wiêksz¹ korelacjê wyliczamy wspó³rzêdne przesuniêcia. Zwizualizuj przesuniêcie analogicznie jak w zadaniu 2.

3.2. SprawdŸ poprawnoœæ detekcji wzorca dla pozosta³ych obróconych  (domek_rxx) i przesuniêtych (domek_sx) obrazów.

3.3. Poka¿ wyniki prowadz¹cemu.