import { Selector } from 'testcafe';

fixture`Demo Login Test`
    .page`https://github.com/login`;

const loginLink = Selector('a').withText('Log in');
const googleOAuthLink = Selector('a.github-icon');
const githubLoginInput = Selector('#login_field');
const githubPasswordInput = Selector('#password');
const githubSignInButton = Selector('input[type="submit"][name="commit"][value="Sign in"]');
const successMessage = Selector('span').withText('Hello, levoducanh8a1');


test('User can log in with valid credentials', async t => {

    await t
        .click(githubLoginInput)
        .typeText(githubLoginInput, 'ducanhlv')
        .click(githubPasswordInput)
        .typeText(githubPasswordInput, 'Ducanh1305@!')
        .click(githubSignInButton) 
        .navigateTo('http://localhost:8000/accounts/login/')
        .click(googleOAuthLink)
        .expect(successMessage.exists).ok('Should show successful login message for cotienxankle');
});

