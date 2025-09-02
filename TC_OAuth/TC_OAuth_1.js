import { Selector } from 'testcafe';

const { BASE_URL } = require('../store');

fixture`Demo Login Test`
    .page`${BASE_URL}`;

const loginLink = Selector('a').withText('Log in');
const googleOAuthLink = Selector('a.google-icon');
const emailInput = Selector('input#identifierId');
const passwordInput = Selector('input[type="password"][name="Passwd"]');

test('User can log in with valid credentials', async t => {
    await t
        .click(loginLink)
        .click(googleOAuthLink)
        .click(emailInput)
        .typeText(emailInput, 'levoducanh8a1@gmail.com')
        .wait(1000000)
        .pressKey('enter')
        .click(passwordInput)
        .typeText(passwordInput, 'Ducanh12a1@')
        .pressKey('enter')
        .wait(10000); // Wait for 10 seconds after submitting the password
});

