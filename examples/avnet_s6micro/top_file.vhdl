library IEEE;
use IEEE.std_logic_1164.all;
library LIB_NAME;
use LIB_NAME.PACKAGE_NAME.all;

entity TOP_NAME is
   port (
      clk_i :  in std_logic;
      led_o : out std_logic
   );
end entity TOP_NAME;

architecture Structural of TOP_NAME is
begin

   dut: CORE_NAME
      generic map (FREQUENCY => 50e6, SECONDS => 1)
      port map (clk_i => clk_i, led_o => led_o);

end architecture Structural;
