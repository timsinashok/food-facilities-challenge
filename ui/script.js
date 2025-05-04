document.addEventListener('DOMContentLoaded', () => {
    // Get references to the forms and results div
    const searchNameForm = document.getElementById('searchNameForm');
    const searchStreetForm = document.getElementById('searchStreetForm');
    const findNearestForm = document.getElementById('findNearestForm');
    const resultsDiv = document.getElementById('results');

    // Helper function to display results
    const displayResults = (data) => {
        resultsDiv.innerHTML = ''; // Clear previous results
        if (!data || data.length === 0) {
            resultsDiv.innerHTML = '<p>No results found.</p>';
            return;
        }

        // Create a list element to hold the results
        const resultList = document.createElement('ul');
        resultList.classList.add('results-list'); // Apply CSS class for list styling

        // Iterate over the data (each food truck item) and create list items
        data.forEach(item => {
            const listItem = document.createElement('li');
            listItem.classList.add('result-item'); // Apply CSS class for item styling

            // --- Create the Summary Section (Always Visible) ---
            const summaryDiv = document.createElement('div');
            summaryDiv.classList.add('result-summary'); // Apply CSS class for summary styling

            // Create span for Applicant Name and Facility Type
            const summaryTitle = document.createElement('span');
            summaryTitle.innerHTML = `<strong>${item.Applicant || 'N/A'}</strong> (${item.FacilityType || 'N/A'})`;
            summaryDiv.appendChild(summaryTitle);

            // Create span for Status (with color class)
            const statusSpan = document.createElement('span');
            statusSpan.classList.add('status'); // Apply base status styling
            // Add a class based on the status value for specific coloring
            statusSpan.classList.add(item.Status ? item.Status.toUpperCase() : 'UNKNOWN'); // Use uppercase for class name
            statusSpan.textContent = item.Status || 'N/A'; // Display status text
            summaryDiv.appendChild(statusSpan);

            listItem.appendChild(summaryDiv); // Add the summary div to the list item

            // --- Create the Details Section (Initially Hidden) ---
            const detailsDiv = document.createElement('div');
            detailsDiv.classList.add('result-details'); // Apply CSS class for details styling

            // Populate the details section with key information from the item
            detailsDiv.innerHTML += `<p><strong>Address:</strong> ${item.Address || 'N/A'}</p>`;
            detailsDiv.innerHTML += `<p><strong>Food Items:</strong> ${item.FoodItems || 'N/A'}</p>`;
            detailsDiv.innerHTML += `<p><strong>Approved:</strong> ${item.Approved || 'N/A'}</p>`;
            detailsDiv.innerHTML += `<p><strong>Expiration Date:</strong> ${item.ExpirationDate || 'N/A'}</p>`;
            detailsDiv.innerHTML += `<p><strong>Location (Lat, Lon):</strong> ${item.Location || 'N/A'}</p>`; // The (lat, lon) string
            detailsDiv.innerHTML += `<p><strong>Latitude:</strong> ${item.Latitude || 'N/A'}</p>`;
            detailsDiv.innerHTML += `<p><strong>Longitude:</strong> ${item.Longitude || 'N/A'}</p>`;
            // If distance_km is present (from the nearest search), display it
            if (item.distance_km !== undefined) { // Check if the property exists
                 detailsDiv.innerHTML += `<p><strong>Distance:</strong> ${item.distance_km.toFixed(2)} km</p>`;
            }
            // Add more details as needed from the item object (e.g., permit, cnn, etc.)
            // detailsDiv.innerHTML += `<p><strong>Permit:</strong> ${item.permit || 'N/A'}</p>`;
            detailsDiv.innerHTML += `<p><strong>CNN:</strong> ${item.cnn || 'N/A'}</p>`;


            listItem.appendChild(detailsDiv); // Add the details div to the list item

            // --- Add Click Listener to Toggle Details ---
            summaryDiv.addEventListener('click', () => {
                // Toggle the display of the details section
                // Check current display state to determine whether to show or hide
                const isHidden = detailsDiv.style.display === 'none' || detailsDiv.style.display === '';
                detailsDiv.style.display = isHidden ? 'block' : 'none'; // Toggle between 'none' and 'block'

                // Toggle the 'expanded' class on the parent list item
                // This class is used by CSS to change the +/- indicator
                listItem.classList.toggle('expanded', isHidden);
            });


            resultList.appendChild(listItem); // Add the complete list item to the results list
        });

        resultsDiv.appendChild(resultList); // Add the results list to the main results div
    };

    // Helper function to handle making API calls using the Fetch API
    const fetchData = async (url) => {
        resultsDiv.innerHTML = '<p>Loading...</p>'; // Show a loading indicator
        try {
            const response = await fetch(url);

            // Check if the HTTP response status is OK (2xx)
            if (!response.ok) {
                // If not OK, try to read the response body for more details
                const errorText = await response.text();
                // Throw an error with status and body for debugging
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
            }

            // Parse the JSON response body
            const data = await response.json();
            // Display the fetched data
            displayResults(data);

        } catch (error) {
            // Catch any errors during the fetch process (network issues, HTTP errors)
            console.error('Error fetching data:', error);
            // Display an error message to the user
            resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    };

    // --- Event Listeners for Form Submissions ---

    // Event listener for the Applicant Name search form
    searchNameForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission (page reload)

        const applicantNameInput = document.getElementById('applicantName');
        const statusSelect = document.getElementById('statusFilter'); // Get the select element

        const applicantName = applicantNameInput.value.trim();
        const status = statusSelect.value; // Get the selected value from the dropdown

        // Basic client-side validation
        if (!applicantName) {
            alert('Please enter an applicant name.');
            applicantNameInput.focus(); // Put focus back on the input
            return;
        }

        // Construct the URL for the search by name endpoint
        let url = `/foodtrucks/search/name?q=${encodeURIComponent(applicantName)}`;
        // Add the status query parameter ONLY if a status is selected (value is not empty)
        if (status) {
            url += `&status=${encodeURIComponent(status)}`;
        }

        // Call the helper function to fetch and display data
        fetchData(url);
    });

    // Event listener for the Street Name search form
    searchStreetForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        const streetNameInput = document.getElementById('streetName');
        const streetName = streetNameInput.value.trim();

        // Basic client-side validation
        if (!streetName) {
            alert('Please enter a street name.');
            streetNameInput.focus();
            return;
        }

        // Construct the URL for the search by street endpoint
        const url = `/foodtrucks/search/street?q=${encodeURIComponent(streetName)}`;

        // Call the helper function to fetch and display data
        fetchData(url);
    });

    // Event listener for the Find Nearest form
    findNearestForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevent the default form submission

        const latitudeInput = document.getElementById('latitude');
        const longitudeInput = document.getElementById('longitude');
        const nearestStatusSelect = document.getElementById('nearestStatusFilter'); // Get the select element
        const limitInput = document.getElementById('limit');

        const latitude = latitudeInput.value.trim();
        const longitude = longitudeInput.value.trim();
        const status = nearestStatusSelect.value; // Get the selected value
        const limit = limitInput.value.trim();

        // Basic client-side validation for required fields
        if (!latitude || !longitude) {
            alert('Please enter both latitude and longitude.');
            if (!latitude) latitudeInput.focus(); else longitudeInput.focus();
            return;
        }

        // Basic client-side validation for numbers
        const latNum = Number(latitude);
        const lonNum = Number(longitude);

        if (isNaN(latNum) || !isFinite(latNum) || isNaN(lonNum) || !isFinite(lonNum)) {
             alert('Please enter valid numbers for latitude and longitude.');
             if (isNaN(latNum) || !isFinite(latNum)) latitudeInput.focus(); else longitudeInput.focus();
             return;
        }

        // Construct the base URL for the nearest endpoint
        let url = `/foodtrucks/nearest?lat=${encodeURIComponent(latNum)}&lon=${encodeURIComponent(lonNum)}`;

        // Add the status query parameter based on the selected value
        // If status is empty (''), send '?status=all' to backend
        // If a specific status is selected, send '?status=<status>'
        // If the default 'APPROVED' is selected, send '?status=APPROVED'
        if (status === '') {
            // If empty value is selected (meaning 'All Statuses' from the dropdown)
            url += `&status=all`; // Send 'all' string to backend
        } else if (status) {
            // If a specific status value is selected (including 'APPROVED')
            url += `&status=${encodeURIComponent(status)}`;
        }
        // If the default 'APPROVED' option was selected and its value was empty,
        // the backend default would apply. But we set value="APPROVED", so it's handled above.


        // Add the limit query parameter if provided and is a valid positive number
        const limitNum = Number(limit);
        if (limit && !isNaN(limitNum) && isFinite(limitNum) && limitNum >= 1) {
             url += `&limit=${encodeURIComponent(limitNum)}`;
        } else if (limit && (isNaN(limitNum) || !isFinite(limitNum) || limitNum < 1)) {
             alert('Please enter a valid limit (a number greater than or equal to 1).');
             limitInput.focus();
             return;
        }
        // If limit input is empty, the backend default (5) is used.

        // Call the helper function to fetch and display data
        fetchData(url);
    });
});
