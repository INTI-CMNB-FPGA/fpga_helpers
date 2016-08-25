library IEEE;
use IEEE.std_logic_1164.all;
library LIB1;
use LIB1.PKG1.all;
use LIB1.PKG2.all;
library LIB2;
use LIB2.PKG1.all;
use LIB2.PKG3.all;

--To test avoid repetition
library LIB1;
use LIB1.PKG1.all;
library LIB2;
use LIB2.PKG1.all;
--End of test section

entity top is
end entity top;
