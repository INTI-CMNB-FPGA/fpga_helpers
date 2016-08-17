library IEEE;
use IEEE.std_logic_1164.all;

entity com1_pkg1_lib2 is
   generic (
      WITH_GENERIC: boolean:=TRUE
   );
   port (
      data_i :  in std_logic;
      data_o : out std_logic
   );
end entity com1_pkg1_lib2;

architecture RTL of com1_pkg1_lib2 is
begin
   data_o <= data_i;
end architecture RTL;
