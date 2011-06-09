

Event.observe(window, 'load', function(ev) {
    col = new collapsables('floatmenu');
    col.addRow('Number of Properties', 'collapsables/num_of_properties.php', {});
    col.addRow('Square Feet', 'collapsables/squarefeet.php', {});
    col.addRow('Annual Impact', '', {});
    col.addRow('Type of Space', '', {});
});
