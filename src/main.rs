extern crate ui;

use ui::{BoxControl, Button, DateTimePicker, Combobox, InitOptions, Label, Window};

fn run() {
    let mainwin = Window::new("Atumate Brewing Instruments", 440, 100, false);
    mainwin.set_margined(true);
    mainwin.on_closing(Box::new(|_| {
        ui::quit();
        false
    }));

    let vbox = BoxControl::new_vertical();
    vbox.set_padded(true);
    mainwin.set_child(vbox.clone().into());

    let hbox_instruments = BoxControl::new_horizontal();
    hbox_instruments.set_padded(true);
    vbox.append(hbox_instruments.clone().into(), false);

    hbox_instruments.append(Label::new("Instrument:").into(), false);

    let instrument_select = Combobox::new();
    instrument_select.append("Instrument 1");
    hbox_instruments.append(instrument_select.into(), false);

    let hbox_dates = BoxControl::new_horizontal();
    hbox_dates.set_padded(true);
    vbox.append(hbox_dates.clone().into(), false);

    hbox_dates.append(Label::new("Select dates to export:").into(), false);

    let start_date = DateTimePicker::new_date_picker();
    hbox_dates.append(start_date.into(), false);

    hbox_dates.append(Label::new(" to ").into(), false);

    let end_date = DateTimePicker::new_date_picker();
    hbox_dates.append(end_date.into(), false);

    let hbox_letsgo = BoxControl::new_horizontal();
    hbox_letsgo.set_padded(true);
    vbox.append(hbox_letsgo.clone().into(), false);

    let export_btn = Button::new("Export Excel");
    hbox_letsgo.append(export_btn.into(), false);

    mainwin.show();
    ui::main();
}

pub fn main() {
    ui::init(InitOptions).unwrap();
    run();
    ui::uninit();
}