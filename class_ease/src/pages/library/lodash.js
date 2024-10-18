import _ from 'lodash';

const convertKeysToSnakeCase = (obj) => {
    const newObj = {};
    Object.keys(obj).forEach((key) => {
        newObj[_.snakeCase(key)] = obj[key];
    });
    return newObj;
};

export default convertKeysToSnakeCase;
