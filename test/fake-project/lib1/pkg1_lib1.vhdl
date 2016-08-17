library IEEE;
use IEEE.std_logic_1164.all;

package pkg1_lib1 is

   component com1_pkg1_lib1 is
      generic (
         WITH_GENERIC: boolean:=TRUE
      );
      port (
         data_i :  in std_logic;
         data_o : out std_logic
      );
   end component com1_pkg1_lib1;

   component com2_pkg1_lib1 is
      port (
         data_i :  in std_logic;
         data_o : out std_logic
      );
   end component com2_pkg1_lib1;

   component com3_pkg1_lib1 is
      generic (
         WITH_GENERIC: boolean:=TRUE
      );
      port (
         data_i :  in std_logic;
         data_o : out std_logic
      );
   end component com3_pkg1_lib1;

end package pkg1_lib1;
