library IEEE;
use IEEE.std_logic_1164.all;

package pkg2_lib1 is

   component com1_pkg2_lib1 is
      generic (
         WITH_GENERIC: boolean:=TRUE
      );
      port (
         data_i :  in std_logic;
         data_o : out std_logic
      );
   end component com1_pkg2_lib1;

end package pkg2_lib1;
