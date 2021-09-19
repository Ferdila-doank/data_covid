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
