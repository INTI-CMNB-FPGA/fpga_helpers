library IEEE;
use IEEE.std_logic_1164.all;

package PACKAGE_NAME is
   component CORE_NAME is
      generic (
         FREQUENCY : positive:=25e6;
         SECONDS   : positive:=1
      );
      port (
         clk_i :  in std_logic;
         rst_i :  in std_logic;
         led_o : out std_logic
      );
   end component CORE_NAME;
end package PACKAGE_NAME;
