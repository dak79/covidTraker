document.addEventListener('DOMContentLoaded', () => {

    /** Sort table
     * 
     * @param {HTMLTableElement} table - The table to sort 
     * @param {number} column - The index of the column to sort
     * @param {boolean} asc - ascending (true) or descending (false) order     
     * @param {HTMLDataElement} type - The type of data to sort (Integer, float or string)
     * 
     * */

    function sortTable(table, column, asc = true, type) {
        const dirModifier = asc ? 1 : -1;
        const tBody = table.tBodies[0];
        const rows = Array.from(tBody.querySelectorAll('tr'));

        // Sort each rows
        const sortedRows = rows.sort((a, b) => {
            const aColText = a.querySelector(`td:nth-child(${column + 1})`).textContent.trim().replace(/,/g, '');
            const bColText = b.querySelector(`td:nth-child(${column + 1})`).textContent.trim().replace(/,/g, '');

            // Check datatype
            if (type == 'integer') {
                return parseInt(aColText) > parseInt(bColText) ? (1 * dirModifier) : (-1 * dirModifier);

            } else if (type == 'float') {
                return parseFloat(aColText) > parseFloat(bColText) ? (1 * dirModifier) : (-1 * dirModifier);
            } else if (type == 'string') {
                return aColText > bColText ? (1 * dirModifier) : (-1 * dirModifier);
            }
        });

        // Remove all rows(tr) from table
        while (tBody.firstChild) {
            tBody.removeChild(tBody.firstChild);
        }

        // Add the sorted rows
        tBody.append(...sortedRows);

        // Remeber how the column is currently sorted
        table.querySelectorAll('th').forEach(th => th.classList.remove('th-sort-asc', 'th-sort-desc'));
        table.querySelector(`th:nth-child(${column + 1})`).classList.toggle('th-sort-asc', asc);
        table.querySelector(`th:nth-child(${column + 1})`).classList.toggle('th-sort-desc', !asc);
    }

    // Click listener on th
    document.querySelectorAll('.table-sortable th').forEach(th => {
        th.addEventListener('click', () => {
            const tableElement = th.parentElement.parentElement.parentElement;
            const thIndex = th.cellIndex;
            const currentAsc = th.classList.contains('th-sort-asc');
            const thType = th.dataset.type;
            sortTable(tableElement, thIndex, !currentAsc, thType);
        });
    });
})