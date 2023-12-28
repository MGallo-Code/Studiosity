/**
 * Extracts the first error message from an Axios error response.
 * Takes into account different error structures (e.g., Django, Nginx).
 * @param {Object} error The error object from Axios.
 * @return {String} The first error message.
 */
export function extractFirstErrorMessage(error) {
    // Check if it's a standard API error response from Django
    if (error.response && error.response.data) {
        const errorKeys = Object.keys(error.response.data);
        if (errorKeys.length > 0 && Array.isArray(error.response.data[errorKeys[0]])) {
            return error.response.data[errorKeys[0]][0];
        }
    }

    // Check for Nginx or other non-JSON error responses
    if (error.response && error.response.status) {
        switch (error.response.status) {
            case 413:
                return "File size must not be larger than 20MB";
            case 504:
                return "Server timeout";
            // Add other cases as needed
            default:
                break;
        }
    }

    return "An unknown error occurred";
}