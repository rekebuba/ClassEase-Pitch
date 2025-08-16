import _ from "lodash";

/**
 * Converts the keys of an object to snake_case.
 *
 * @param {Object} obj - The object whose keys need to be converted.
 * @returns {Object} A new object with the keys converted to snake_case.
 */
const convertKeysToSnakeCase = (obj) => {
  const newObj = {};
  Object.keys(obj).forEach((key) => {
    newObj[_.snakeCase(key)] = obj[key];
  });
  return newObj;
};

export default convertKeysToSnakeCase;
