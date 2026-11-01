# Circuit description: filter and gain stage

Second-order Sallen-Key low-pass followed by a non-inverting gain stage

17 physical components; power symbols and ERC flags are excluded from that count.

| Reference | KiCad symbol | Value | Electrical role |
|---|---|---|---|
| U1 | Amplifier_Operational:TL081 | TL081 | Active filter amplifier |
| U2 | Amplifier_Operational:TL081 | TL081 | Non-inverting output gain amplifier |
| R1 | Device:R | 15.8k | First frequency-setting series resistor |
| R2 | Device:R | 15.8k | Second frequency-setting series resistor |
| R3 | Device:R | 10k | U1 gain reference to ground |
| R4 | Device:R | 5.90k | U1 negative feedback |
| R5 | Device:R | 10k | U2 gain reference to ground |
| R6 | Device:R | 10k | U2 negative feedback |
| C1 | Device:C | 10n | Frequency-dependent feedback from U1 output to RC junction |
| C2 | Device:C | 10n | Filter shunt capacitor |
| C3 | Device:C | 100n | U1 positive supply bypass |
| C4 | Device:C | 100n | U1 negative supply bypass |
| C5 | Device:C | 100n | U2 positive supply bypass |
| C6 | Device:C | 100n | U2 negative supply bypass |
| J1 | Connector_Generic:Conn_01x02 | INPUT | Pin 1 signal, pin 2 ground |
| J2 | Connector_Generic:Conn_01x02 | OUTPUT | Pin 1 signal, pin 2 ground |
| J3 | Connector_Generic:Conn_01x03 | SUPPLY | Pin 1 +12V, pin 2 GND, pin 3 -12V |

## Connections specified before drawing

| Node | Connected component/pin pairs |
|---|---|
| input | J1/1, R1/1 |
| filter_junction | R1/2, R2/1, C1/1 |
| filter_sense | R2/2, C2/1, U1/3 |
| filter_output | U1/6, C1/2, R4/2, U2/3 |
| U1_feedback | U1/2, R3/1, R4/1 |
| output | U2/6, R6/2, J2/1 |
| U2_feedback | U2/2, R5/1, R6/1 |
| +12V | J3/1, U1/7, U2/7, C3/1, C5/1 |
| -12V | J3/3, U1/4, U2/4, C4/1, C6/1 |
| GND | J3/2, J1/2, J2/2, R3/2, R5/2, C2/2, C3/2, C4/2, C5/2, C6/2 |

Intentionally unconnected: U1/1, U1/5, U1/8, U2/1, U2/5, U2/8

## Functional relationships and drawing patterns

- main signal: Continuous left-to-right wires.
- frequency dependent feedback: Upper loop around U1 input network.
- negative feedback: Lower loop around U1.
- negative feedback: Lower loop around U2.
- gain reference: Vertical resistor below each feedback node.
- filter shunt: Vertical branch clear of U1 feedback.
- decoupling: Two clearly identified bypass pairs; shared power symbols.

## Assumptions

- External regulated +/-12 V supply
- Low-impedance input source and high-impedance output load
- Nominal ideal filter f0 approximately 1.007 kHz; Q approximately 0.709
- Filter gain 1.59 V/V, output-stage gain 2 V/V, combined passband gain 3.18 V/V
- Drawing and connectivity test; no simulation or hardware validation

[Filter topology and equations: TI SLOA024B](https://www.ti.com/lit/an/sloa024b/sloa024b.pdf)
