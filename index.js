const { inspect } = require("util");
const core = require("@actions/core");
const exec = require("@actions/exec");
const setupPython = require("./src/setup-python");

async function run() {
  try {
    // Allows ncc to find assets to be included in the distribution
    const src = __dirname + "/src";
    core.debug(`src: ${src}`);

    // Setup Python from the tool cache
    setupPython("3.8.x", "x64");

    // Install vendored dependencies
    await exec.exec("pip", [
      "install",
      "--requirement",
      `${src}/requirements.txt`,
      "--no-index",
      `--find-links=${__dirname}/vendor`
    ]);

    // Fetch action inputs
    const inputs = {
      slugs: core.getMultilineInput("slugs"),
      format: core.getInput("format"),
      output: core.getInput("output"),
      id: core.getInput("id"),
      sort: core.getBooleanInput("sort"),
      random: core.getInput("random"),
      style: core.getInput("style"),
      verify: core.getBooleanInput("verify")
    };
    core.debug(`Inputs: ${inspect(inputs)}`);

    // Execute python script
    await exec.exec("python", [
      `${src}/icons.py`,
      // add inputs.slugs if not just whitespace
      /^\s*$/.test(inputs.slugs) ? "" : `--slugs=${inputs.slugs}`,
      /^\s*$/.test(inputs.output) ? "" : `--output=${inputs.output}`,
      `--format=${inputs.format}`,
      `--id=${inputs.id}`,
      `--random=${inputs.random}`,
      `--badge-style=${inputs.style}`,
      inputs.verify ? '--verify' : "",
      inputs.sort ? "" : "--no-hilbert"
    ]);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
