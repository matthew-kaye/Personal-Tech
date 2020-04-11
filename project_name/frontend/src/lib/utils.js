export function generateValidationErrorMessage(
  validationErrors,
  action = "being able to continue"
) {
  /*
          TODO:
          This function should likely exist as a component.
      */
  const fieldsWithErrors = Object.keys(validationErrors).length;
  if (fieldsWithErrors === 1) {
    return `There is 1 issue that must be resolved before ${action}. It has been highlighted in the form above.`;
  } else {
    return `There are ${fieldsWithErrors} issues that must be resolved before ${action}. They have been highlighted in the form above.`;
  }
}

export function validatePassword(password) {
  const errors = [];
  if (password === undefined || password === null || password.length < 6) {
    errors.push("A password must be 8 characters or longer.");
  } else if (password.length > 100) {
    errors.push("A password must be less than 100 characters in length.");
  }
  return errors;
}
