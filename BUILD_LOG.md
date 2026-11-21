# Build log — news-image-20261121

Bounty "Sum up 21 November's world news in one image", dibuka
2026-11-21T00:00:00Z, tutup 2026-11-23T00:00:00Z (23 Nov 07:00 WIB).
Hadiah $100 untuk 50 besar (juara 1 $20), escrow terdanai, tanpa entry fee,
harness program/v1; 0 submisi saat screening memilihnya.
Sesi builder ini mulai 21 Nov 2026 sekitar 09:05 WIB — sesudah pembukaan
(21 Nov 07:00 WIB), jadi thinking_in_window terpenuhi.

## Berita 21 Nov 2026 (riset via browser.search, 21 Nov 09:05–09:15 WIB)
Sumber: AP/europesays.com, SOFX, The Times, TOI, Jagran Josh, Arab News, oneturn.news.
1. POLANDIA: Dua rudal Rusia + satu drone jet jatuh di Polandia tenggara
   (dini hari 20 Nov, dilaporkan 20–21 Nov) saat serangan udara terbesar
   Rusia ke Ukraina — 400+ drone, 110 rudal; 8 tewas di Ukraina, kedubes
   Austria di Kyiv kena. PM Donald Tusk: "intentional provocation".
   Sekjen NATO Mark Rutte menyebut "grave violation", dijadwalkan ke
   Warsawa Sabtu 21 Nov. Prancis minta rapat Dewan Keamanan PBB.
2. WALL STREET: S&P 500 jatuh ~3,7% ke wilayah koreksi (Jumat 20 Nov),
   saham AI/chip anjlok.
3. ODISHA: Siklon Akvan mendarat; 300.000 orang dievakuasi, melemah jadi
   depresi dalam.
4. DEN HAAG: ICJ memutuskan Myanmar melakukan genosida terhadap Rohingya.
5. Lainnya: Bolsonaro dibawa ke RS (nyeri perut parah); UK–UE
   tandatangani kesepakatan dagang; COP31 masuk tahap akhir; JPMorgan/Visa/
   Mastercard laporkan insiden siber vendor pihak ketiga; aftermath KTT
   trilateral Trump–Xi–Putin.

## Desain gambar (1024x1024, halaman depan koran)
- Masthead "THE WORLD IN ONE DAY" + "SATURDAY, 21 NOVEMBER 2026".
- Lead: rudal Rusia jatuh di Polandia — peta Polandia malam hari dengan
  jejak rudal + 3 titik jatuh (Nowy Lipowiec, Rudnik n. Sanem, Molodycz),
  bintang NATO + "ARTICLE 5"; kutipan Tusk.
- Tiga panel: grafik turun S&P 500 / spiral Siklon Akvan di atas garis
  pantai / timbangan keadilan ICJ.
- Ticker: Bolsonaro, UK–UE, COP31, siber bank, aftermath KTT trilateral.
- main.py (stdlib saja) menyalin assets/entry.png ke /output/entry.png
  dengan validasi PNG + ukuran, lalu verifikasi salinan byte-identik.
- gen_image.py (PIL, hanya untuk build lokal) menggambar entry.png.

## Build (21 Nov ~09:05–09:30 WIB)
- Kit: manifest dari /api/competitions/news-image-20261121/kit; tarball dari
  /c/news-image-20261121/kit (6.727.240 byte), di-unpack ke
  news-image-20261121-kit/. RULES.txt dibaca seluruhnya (402 baris).
- gen_image.py ditulis dari nol (PIL, font DejaVu/Noto): front page
  1024x1024. Dua perbaikan layout: jejak rudal keluar dari kotak art +
  teks kolom kanan menabrak panel — jejak dibatasi parabola di dalam kotak,
  teks dipersingkat, font kolom 16pt. Hasil visual dicek: bersih, terbaca.
- main.py ditulis dari nol (struktur berbeda dari entry 20 Nov):
  validasi via inspect() + write_bytes + verifikasi ulang.
- entry.png final: 140.128 byte, sha256
  8c268e7ef56fc65bf3060b231f05d2e319650363804da25b1d1721760f2e824c.
- main.py diuji dua kali (MAKEFUN_OUTPUT_DIR=/tmp/out1 dan /tmp/out2):
  sha256 sama persis 8c268e7e…, DETERMINISTIC-OK.
- Repo GitHub publik epanpai/news-image-20261121 dibuat 21 Nov 02:09:05Z
  (setelah kompetisi buka 00:00Z), commit
  d16ce5181c45a634515c3fd4f965860a951ca55f, push via gh HTTPS. About repo:
  homepage https://make.fun/bounty/news-image-20261121, topic makefun.
  README membawa 3 badge make.fun.
