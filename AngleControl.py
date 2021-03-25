from traits.api import HasTraits, CInt, Instance, Property, Range
from traitsui.api import View, Group, HGroup, Item

from TaitBryanRotation import ElementalRotationDefinition


class AngleControl(HasTraits):
    '''
    Euler angle UI elements:

    Angles in the UI can be set by
    1. initial:     Typing the desired angle
    2. add_diff:    Once the first angle is chosen, the camera can be moved using a slider

    final = angle + d_angle will be displayed and is intended to be used in subsequent actions
    '''

    definition = Instance(ElementalRotationDefinition, ())

    # Large scale rotation angle
    initial = CInt(0)

    # Small scale rotation angle slider
    add_diff = Range(-50,50, 0)

    # Resulting rotation angle
    final = Property(observe='initial, add_diff')
    def _get_final(self):
        return self.initial + self.add_diff

    # UI elements
    label = Property(depends_on='definition.name')
    def _get_label(self):
        return self.definition.angle_name + ": "

    view_label = Item('label', show_label=False, style="readonly")
    view_initial = Item('initial', show_label=False)
    view_add_diff = HGroup(Item('', label="+"), Item('add_diff', show_label=False, width=200))
    view_final = HGroup(Item('', label="="), Item('final', show_label=False, style = "readonly", width=40))

    view = View(HGroup(view_label,
                       view_initial,
                       view_add_diff,
                       view_final, show_border=True, springy=True))


class AngleControlPanel(HasTraits):
    '''
    Euler angle UI elements:

    Angles in the UI can be set by
    1. angle:       Typing the desired angle
    2. d_angle: Once the first angle is chosen, the camera can be moved using a slider

    angle_total = angle + d_angle will be used in the visualization.

    Note concerning implementation: It would seem cleaner to use a map or list.
    However I am not aware of any intuitive traits editor factory, that would give
    GUI elements like: key(order): value(AngleControl()).
    '''

    angle_applied_first = Instance(AngleControl(),())
    angle_applied_second = Instance(AngleControl(), ())
    angle_applied_last = Instance(AngleControl(), ())

    view = View(Group(Item("20"),
                       Item('angle_applied_first', style="custom", label="1."),
                       Item("20"),
                       Item('angle_applied_second', style="custom", label="2."),
                       Item("20"),
                       Item('angle_applied_last', style="custom", label="3."),
                       Item("20"), springy=True))
