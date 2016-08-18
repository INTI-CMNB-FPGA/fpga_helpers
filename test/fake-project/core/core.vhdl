library IEEE;
use IEEE.std_logic_1164.all;

library LIB1;
use LIB1.pkg1_lib1.all;
library LIB2;
use LIB2.pkg1_lib2.all;

entity core is
   generic (
      WITH_GENERIC: boolean:=TRUE
   );
   port (
      data_i :  in std_logic;
      data_o : out std_logic
   );
end entity core;

architecture RTL of core is
   signal data : std_logic;
begin

   com2_pkg1_lib1_inst: com2_pkg1_lib1
      port map (
         data_i => data_i,
         data_o => data
      );

   com1_pkg1_lib2_inst: com1_pkg1_lib2
      generic map (WITH_GENERIC => FALSE)
      port map (
         data_i => data,
         data_o => data_o
      );

end architecture RTL;
