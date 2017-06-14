library IEEE;
use IEEE.std_logic_1164.all;

entity CORE_NAME is
   generic (
      FREQUENCY : positive:=25e6;
      SECONDS   : positive:=1
   );
   port (
      clk_i :  in std_logic;
      led_o : out std_logic
   );
end entity CORE_NAME;

architecture RTL of CORE_NAME is
   constant DIV : positive:=FREQUENCY*SECONDS-1;
   signal   led : std_logic;
begin
   blink:
   process (clk_i)
      variable cnt: natural range 0 to DIV:=0;
   begin
      if rising_edge(clk_i) then
         if cnt=DIV then
            cnt:=0;
            led <= not(led);
         else
            cnt:=cnt+1;
         end if;
      end if;
   end process blink;
   led_o <= led;
end architecture RTL;
