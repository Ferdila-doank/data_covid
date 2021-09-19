CREATE TABLE public.data_covid (
	tanggal timestamp NULL,
	"KASUS" int8 NULL,
	"MENINGGAL" int8 NULL,
	"SEMBUH" int8 NULL,
	"DIRAWAT_OR_ISOLASI" int8 NULL,
	"AKUMULASI_KASUS" int8 NULL,
	"AKUMULASI_SEMBUH" int8 NULL,
	"AKUMULASI_MENINGGAL" int8 NULL,
	"AKUMULASI_DIRAWAT_OR_ISOLASI" int8 NULL,
	last_date timestamp NULL,
	provinsi text NULL
);

CREATE TABLE public.last_update_covid (
	tanggal timestamp NULL,
	"AKUMULASI_KASUS" int8 NULL,
	"AKUMULASI_SEMBUH" int8 NULL,
	"AKUMULASI_MENINGGAL" int8 NULL,
	"AKUMULASI_DIRAWAT_OR_ISOLASI" int8 NULL,
	last_date timestamp NULL,
	provinsi text NULL
);

CREATE TABLE public.provinsi (
	prov_name text NULL
);

INSERT INTO public.provinsi (prov_name) VALUES
	 ('DKI_JAKARTA'),
	 ('JAWA_BARAT'),
	 ('JAWA_TIMUR'),
	 ('JAWA_TENGAH'),
	 ('BANTEN'),
	 ('DAERAH_ISTIMEWA_YOGYAKARTA'),
	 ('BALI'),
	 ('KALIMANTAN_TIMUR'),
	 ('KALIMANTAN_SELATAN'),
	 ('KALIMANTAN_TENGAH');
INSERT INTO public.provinsi (prov_name) VALUES
	 ('KALIMANTAN_BARAT'),
	 ('KALIMANTAN_UTARA'),
	 ('SUMATERA_UTARA'),
	 ('SUMATERA_BARAT'),
	 ('SUMATERA_SELATAN'),
	 ('LAMPUNG'),
	 ('KEPULAUAN_BANGKA_BELITUNG'),
	 ('ACEH'),
	 ('JAMBI'),
	 ('SULAWESI_UTARA');
INSERT INTO public.provinsi (prov_name) VALUES
	 ('SULAWESI_TENGAH'),
	 ('SULAWESI_TENGGARA'),
	 ('SULAWESI_SELATAN'),
	 ('SULAWESI_BARAT'),
	 ('KEPULAUAN_RIAU'),
	 ('RIAU'),
	 ('NUSA_TENGGARA_TIMUR'),
	 ('NUSA_TENGGARA_BARAT'),
	 ('PAPUA'),
	 ('PAPUA_BARAT');
INSERT INTO public.provinsi (prov_name) VALUES
	 ('BENGKULU'),
	 ('MALUKU'),
	 ('MALUKU_UTARA'),
	 ('GORONTALO');
