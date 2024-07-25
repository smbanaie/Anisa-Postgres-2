--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.0
-- Dumped by pg_dump version 9.6.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: countries; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE countries (
    continent text,
    country text
);


ALTER TABLE countries OWNER TO postgres;

--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY countries (continent, country) FROM stdin;
Africa	Algeria
Africa	Angola
Africa	Benin
Africa	Botswana
Africa	Burkina
Africa	Burundi
Africa	Cameroon
Africa	Cape Verde
Africa	Central African Republic
Africa	Chad
Africa	Comoros
Africa	Congo
Africa	Djibouti
Africa	Egypt
Africa	Equatorial Guinea
Africa	Eritrea
Africa	Ethiopia
Africa	Gabon
Africa	Gambia
Africa	Ghana
Africa	Guinea
Africa	Guinea-Bissau
Africa	Ivory Coast
Africa	Kenya
Africa	Lesotho
Africa	Liberia
Africa	Libya
Africa	Madagascar
Africa	Malawi
Africa	Mali
Africa	Mauritania
Africa	Mauritius
Africa	Morocco
Africa	Mozambique
Africa	Namibia
Africa	Niger
Africa	Nigeria
Africa	Rwanda
Africa	Sao Tome and Principe
Africa	Senegal
Africa	Seychelles
Africa	Sierra Leone
Africa	Somalia
Africa	South Africa
Africa	South Sudan
Africa	Sudan
Africa	Swaziland
Africa	Tanzania
Africa	Togo
Africa	Tunisia
Africa	Uganda
Africa	Zambia
Africa	Zimbabwe
Asia	Afghanistan
Asia	Bahrain
Asia	Bangladesh
Asia	Bhutan
Asia	Brunei
Asia	Burma (Myanmar)
Asia	Cambodia
Asia	China
Asia	East Timor
Asia	India
Asia	Indonesia
Asia	Iran
Asia	Iraq
Asia	Israel
Asia	Japan
Asia	Jordan
Asia	Kazakhstan
Asia	North Korea
Asia	South Korea
Asia	Kuwait
Asia	Kyrgyzstan
Asia	Laos
Asia	Lebanon
Asia	Malaysia
Asia	Maldives
Asia	Mongolia
Asia	Nepal
Asia	Oman
Asia	Pakistan
Asia	Philippines
Asia	Qatar
Asia	Russian Federation
Asia	Saudi Arabia
Asia	Singapore
Asia	Sri Lanka
Asia	Syria
Asia	Tajikistan
Asia	Thailand
Asia	Turkey
Asia	Turkmenistan
Asia	United Arab Emirates
Asia	Uzbekistan
Asia	Vietnam
Asia	Yemen
Europe	Albania
Europe	Andorra
Europe	Armenia
Europe	Austria
Europe	Azerbaijan
Europe	Belarus
Europe	Belgium
Europe	Bosnia and Herzegovina
Europe	Bulgaria
Europe	Croatia
Europe	Cyprus
Europe	Czech Republic
Europe	Denmark
Europe	Estonia
Europe	Finland
Europe	France
Europe	Georgia
Europe	Germany
Europe	Greece
Europe	Hungary
Europe	Iceland
Europe	Ireland
Europe	Italy
Europe	Latvia
Europe	Liechtenstein
Europe	Lithuania
Europe	Luxembourg
Europe	Macedonia
Europe	Malta
Europe	Moldova
Europe	Monaco
Europe	Montenegro
Europe	Netherlands
Europe	Norway
Europe	Poland
Europe	Portugal
Europe	Romania
Europe	San Marino
Europe	Serbia
Europe	Slovakia
Europe	Slovenia
Europe	Spain
Europe	Sweden
Europe	Switzerland
Europe	Ukraine
Europe	United Kingdom
Europe	Vatican City
North America	Antigua and Barbuda
North America	Bahamas
North America	Barbados
North America	Belize
North America	Canada
North America	Costa Rica
North America	Cuba
North America	Dominica
North America	Dominican Republic
North America	El Salvador
North America	Grenada
North America	Guatemala
North America	Haiti
North America	Honduras
North America	Jamaica
North America	Mexico
North America	Nicaragua
North America	Panama
North America	Saint Kitts and Nevis
North America	Saint Lucia
North America	Saint Vincent and the Grenadines
North America	Trinidad and Tobago
North America	United States
Oceania	Australia
Oceania	Fiji
Oceania	Kiribati
Oceania	Marshall Islands
Oceania	Micronesia
Oceania	Nauru
Oceania	New Zealand
Oceania	Palau
Oceania	Papua New Guinea
Oceania	Samoa
Oceania	Solomon Islands
Oceania	Tonga
Oceania	Tuvalu
Oceania	Vanuatu
South America	Argentina
South America	Bolivia
South America	Brazil
South America	Chile
South America	Colombia
South America	Ecuador
South America	Guyana
South America	Paraguay
South America	Peru
South America	Suriname
South America	Uruguay
South America	Venezuela
\.

--
-- Name: idx_continent; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_continent ON countries USING btree (continent);

--
-- PostgreSQL database dump complete
--
