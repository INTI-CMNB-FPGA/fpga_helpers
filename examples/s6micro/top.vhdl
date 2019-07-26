library IEEE;
use IEEE.std_logic_1164.all;
library Examples;
use Examples.examples.all;

entity Top is
   port (
      clk_i :  in std_logic;
      led_o : out std_logic
   );
end entity Top;

architecture Structural of Top is
begin

   dut: Blinking
      generic map (FREQ => 50e6, SECS => 1)
      port map (clk_i => clk_i, led_o => led_o);

end architecture Structural;
