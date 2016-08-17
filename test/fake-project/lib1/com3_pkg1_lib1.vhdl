library IEEE;
use IEEE.std_logic_1164.all;

entity com3_pkg1_lib1 is
   generic (
      WITH_GENERIC: boolean:=TRUE
   );
   port (
      data_i :  in std_logic;
      data_o : out std_logic
   );
end entity com3_pkg1_lib1;

architecture RTL of com3_pkg1_lib1 is
begin
   data_o <= data_i;
end architecture RTL;