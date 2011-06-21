import nineml.abstraction_layer as al

def get_component():
    subthreshold_regime = al.Regime(
        "dV/dt = (-gL*(V-vL) + Isyn)/C",
        transitions = al.On("V> theta",
                                do=["t_spike = t", "V = V_reset",
                                    al.SpikeOutputEvent],
                                to="refractory_regime"),
        name="subthreshold_regime"
        )

    refractory_regime = al.Regime(
        transitions = al.On("t >= t_spike + t_ref",
                                to=subthreshold_regime),
        name="refractory_regime"
        )

    analog_ports = [al.SendPort("V"),
             al.ReducePort("Isyn",reduce_op="+")]

    c1 = al.ComponentClass("LeakyIAF", regimes = [subthreshold_regime, refractory_regime], analog_ports=analog_ports)

    return c1
