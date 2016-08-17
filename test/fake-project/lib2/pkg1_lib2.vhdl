library IEEE;
use IEEE.std_logic_1164.all;

package pkg1_lib2 is

   component com1_pkg1_lib2 is
      generic (
         WITH_GENERIC: boolean:=TRUE
      );
      port (
         data_i :  in std_logic;
         data_o : out std_logic
      );
   end component com1_pkg1_lib2;

end package pkg1_lib2;
