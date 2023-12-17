// errorHandler.js

/**
 * Extracts the first error message from an Axios error response.
 * @param {Object} error The error object from Axios.
 * @return {String} The first error message.
 */
export function extractFirstErrorMessage(error) {
    if (error.response && error.response.data) {
        const errorKeys = Object.keys(error.response.data);
        if (
            errorKeys.length > 0 &&
            error.response.data[errorKeys[0]].length > 0
        ) {
            return error.response.data[errorKeys[0]][0];
        }
    }
    return "An unknown error occurred";
}
