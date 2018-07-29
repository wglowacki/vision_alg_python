Transformata Fouriera-Mellina
1. Cel zaj��
wyszukiwanie wzorc�w za pomoc�  transformaty Fouriera-Mellina
2. Wyszukiwanie wzorca za pomoc� korelacji
2.1.Ze strony kursu pobierz archiwum z danymi do �wiczenia i rozpakuj je we w�asnym katalogu roboczym. UWAGA - W dzisiejszym �wiczeniu do wy�wietlania obraz�w lepiej jest u�ywa� funkcji imshow z modu�u pyplot, a nie cv2.

2.2. Utw�rz nowy skrypt. Wyszukaj wzorzec zapisany w obrazie 'wzor.pgm' na przeszukiwanym obrazie 'domek_r0.pgm'. Oba obrazy wczytaj w  odcieniach szaro�ci. Zacznij od uzupe�nienia obraz wzorca zerami do rozmiaru obrazu przeszukiwanego (funkcja np.zeros(shape)). Najlepiej zrobi� to tak, aby �rodek wzorca znalaz� si� w punkcie (0,0) - w�wczas maksimum korelacji wska�e po�o�enie wzorca na obrazie przeszukiwanym (podpowied� - mozna najpierw wzorzec umie�ci� tak, aby jego �rodek pokry� si� ze �rodkiem obrazu, a nast�pnie wykona� fftshift). Przeprowad� korelacj� obrazu przeszukiwanego i obrazu wzorca z zerami w dziedzinie cz�stotliwo�ci. Do wyliczenia transformaty Fouriera wykorzystaj funkcje fft2 i fftshift z modu�u numpy.fft, a do transformaty odwrotnej ifft2 i ifftshift (z tego samego modu�u). Wsp�rz�dne maksimum w obrazie modu�u transformaty odwrotnej mo�na uzyska� np. przy u�yciu instrukcji:

 y,x = np.unravel_index( np.argmax(modul_odwrotnej), modul_odwrotnej.shape)

Modu� liczby zespolonej uzyskujemy za pomoc� funkcji np.abs.

Sprawd�, czy maksimum wypada w miejscu wyst�powania wzorca na obrazie przeszukiwanym (raczej nie powinno).

2.3. Zmie� korelacj� na korelacj� fazow�. Sprawd�, czy maksimum wypada w miejscu wyst�powania wzorca na obrazie przeszukiwanym (teraz powinno by� dobrze).

2.4. Zwizualizuj przesuni�cie przrekszta�caj�c obraz wzorca z zerami (przed fftshift)  za pomoc� funkcji realizuj�cej przekszta�cenie afiniczne - cv2.warpAffine. Przyk�adowy kod:

macierz_translacji = np.float32([[1,0,dx],[0,1,dy]])  - gdzie dx, dy - wektor przesuni�cia
obraz_przesuniety = cv2.warpAffine(obraz_wzorca_z, macierz_translacji, (obraz_wzorca_z.shape[1], obraz_wzorca_z.shape[0]))

Wektor przesuniecia, o ile �rodek wzorca znajdowa� si� w punkcie (0,0), to:

dx = x - size_x //2

dy = y - size_y//2 

2.5. Poka� wyniki prowadz�cemu

3. Wyszukiwanie wzorca niezale�nie od obrotu i skali
3.1 Wczytaj obraz przeszukiwany 'domek_r30.pgm' oraz obraz wzorca 'domek_r0_64.pgm'. Uzupe�nij zerami obraz wzorca tak jak w punkcie 2.

Zrealizuj obliczenia z poni�szego schematu uwzgl�dniaj�c nast�puj�ce uwagi:



- Uzupe�nij zerami mniejszy obraz tak jak w punkcie 2 ale z uwzgl�dnieniem okna Hanninga uzyskanym funkcj�:

def hanning2D(n):
    h = np.hanning(n)
    return np.sqrt(np.outer(h,h))

Okno przemna�amy przez obraz przed uzupe�nieniem go zerami. n to rozmiar obrazu w pionie lub poziomie (zak�adamy, �e s� takie same)

- Przed transformacj� log-polar przefiltruj obrazy filtrem g�rnoprzepustowym uzyskanym funkcj�:

def highpassFilter(size):
    rows = np.cos(np.pi*np.matrix([-0.5 + x/(size[0]-1) for x in range(size[0])]))
    cols = np.cos(np.pi*np.matrix([-0.5 + x/(size[1]-1) for x in range(size[1])]))
    X = np.outer(rows,cols)
    return (1.0 - X) * (2.0 - X)

size to shape obrazu filtrowanego. Filtrujemy w dziedzinie cz�stotliwo�ci, a wi�c polega to na przemno�eniu obraz�w amplitud przez filtr.

- Transformat� log-polar mo�na zrealizowa� za pomoc� funkcji cv2.logPolar. �rodek przekszta�cenia to �rodek obrazu, natomiast parametr M prosz� ustawi� na:   2*R/np.log(R) gdzie R to max. promie�, czyli po�owa rozmiaru pionowego lub poziomego. Parametr flags to: cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS.

- Uzyskane w wyniku pierwszej korelacji fazowej wsp�rz�dne maksimum (wsp_kata, wsp_logr) przeliczamy na  skalowanie i stopnie wg wzor�w:

skala = np.exp(1/M) ** wykl  -  gdzie M to parametr funkcji cv2.logPolar, a wykl wyliczamy jako:

    if wsp_logr > np_fimlp.shape[1]//2:
        wykl =rozmiar_wsp_logr - wsp_logr
    else:
        wykl = - wsp_logr

kat1  =  360 - A                             - gdzie    A =  (wsp_kata * 360.0 ) / rozmiar_wsp_kata

kat2  =  360 - A - 180

K�ty s� dwa, gdy� ze wzgl�du na symetri� modu�u widma cz�stotliwo�ciowego wykrywane s� obroty tylko do 180 stopni. Dlatego w nastepnym kroku trzeba sprawdzi� oba k�ty i wybra� ten, kt�ry daje lepsz� korelacj�.

- Wyliczone k�ty i skal� nale�y u�y� w przekszta�ceniu afinicznym, podobnie jak w zadaniu 2. Tym razem macierz translacji b�dzie wygl�da�a nast�puj�co:

macierz_translacji = cv2.getRotationMatrix2D((srodekTrans[0], srodekTrans[1]), kat, skala) gdzie srodekTrans to �rodek obrazu:
srodekTrans = [math.floor((obraz.shape[0] + 1) / 2), math.floor((obraz.shape[1] + 1 ) / 2)]


 - Przetransformowane obrazy nale�y podda� transformacie Fouriera i  skorelowa� z widmemem obrazu przeszukiwanego. Z wyniku daj�cego wi�ksz� korelacj� wyliczamy wsp�rz�dne przesuni�cia. Zwizualizuj przesuni�cie analogicznie jak w zadaniu 2.

3.2. Sprawd� poprawno�� detekcji wzorca dla pozosta�ych obr�conych  (domek_rxx) i przesuni�tych (domek_sx) obraz�w.

3.3. Poka� wyniki prowadz�cemu.