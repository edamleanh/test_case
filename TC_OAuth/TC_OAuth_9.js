import { Selector } from 'testcafe';

fixture`Demo Login Test`
    .page`http://localhost:8000`;

const loginLink = Selector('a').withText('Log in');
const googleOAuthLink = Selector('a.github-icon');
const githubLoginInput = Selector('#login_field');
const githubPasswordInput = Selector('#password');
const githubSignInButton = Selector('input[type="submit"][name="commit"][value="Sign in"]');
const successMessage = Selector('span').withText('Hello, cotienxankle.');
const authorizeButton = Selector('button.js-oauth-authorize-btn').withText('Authorize edamleanh');

test('User can log in with valid credentials', async t => {

    await t
        .click(loginLink)
        .click(googleOAuthLink)
        .click(githubLoginInput)
        .typeText(githubLoginInput, 'cotienxankle')
        .click(githubPasswordInput)
        .typeText(githubPasswordInput, 'Ducanh1305@!')
        .click(githubSignInButton)
        .wait(1000) // Wait for the page to load after GitHub login
        .click(authorizeButton)
        .expect(successMessage.exists).ok('Should show successful login message for cotienxankle');

});

