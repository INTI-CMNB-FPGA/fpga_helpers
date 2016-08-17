library IEEE;
use IEEE.std_logic_1164.all;

library LIB1;
use LIB1.pkg1_lib1.all;

entity com2_pkg1_lib1 is
   port (
      data_i :  in std_logic;
      data_o : out std_logic
   );
end entity com2_pkg1_lib1;

architecture RTL of com2_pkg1_lib1 is
begin

   inst: com1_pkg1_lib1
      generic map (WITH_GENERIC => FALSE)
      port map (
         data_i => data_i,
         data_o => data_o
      );

end architecture RTL;
