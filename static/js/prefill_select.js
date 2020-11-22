function select_option_with_value(option_id, value) {
    let select = document.getElementById(option_id);

    for (let i = 0; i < select.length; i++) {
        option = select[i];
        if (option.value == value) {
            console.log(
                `selecting option - Value:${option.value} Name:${option.textContent} for ${select.name}`
            );
            option.selected = true;
        }
    }
}
