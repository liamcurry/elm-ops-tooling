#!/usr/bin/env ruby

require 'English'
require 'pty'

=begin
  Runs package install until it succeeds or fails 10 times in a row.

  Test cases for testing manually:

  # fails permanently
  $ ./with_retry.rb ruby -e 'raise "Hello"'
  $ ./with_retry.rb ruby -e 'exit 2'

  # command not found
  $ ./with_retry.rb non-existent-command

  # succeeds
  $ ./with_retry.rb ruby -e 'exit 0'
  $ ./with_retry.rb ruby -e 'sleep(1); now = `date +%s`.to_i; goal = ARGV[0].to_i + 5; puts "#{now} > #{goal}"; exit (now > goal)' `date +%s`
=end

def run_command_with_retry(command_and_args)
  exit_status = nil
  last_exception = nil
  10.times do |i|
    begin
      last_exception, exit_status = run_command command_and_args
      exit 0 if exit_status == 0
    rescue Errno::ENOENT
      puts "#{command_and_args.first}: command not found"
      exit 1
    rescue => e
      exit_status = e
    end
    puts "Attempt ##{i} failure: #{exit_status.class}:\n#{exit_status}"
  end

  puts "Permanently failed to execute: #{command_and_args.join(' ')}"
  puts "Last exception from #run_command was: \n #{last_exception.class}: #{last_exception}" if last_exception
  exit 1
end

def run_command(command_and_args)
  last_exception = nil
  status = nil

  begin
    PTY.spawn(*command_and_args) do |stdout, _stdin, pid|
      begin
        stdout.each { |line| print line }
      rescue Errno::EIO => e
        # Errno:EIO error, but this probably just means
        # that the process has finished giving output
        last_exception = e
      ensure
        # ref:
        # http://stackoverflow.com/a/10306782/20226
        # http://stackoverflow.com/a/7263243/20226
        _pid, status = Process.wait2 pid
      end
    end

    # ref:
    # http://www.shanison.com/2010/09/11/ptychildexited-exception-and-ptys-exit-status/
    if status.nil?
      status = if $ERROR_INFO.nil? || $ERROR_INFO.is_a?(SystemExit) && $ERROR_INFO.success?
                 0
               else
                 $ERROR_INFO.is_a?(SystemExit) ? $ERROR_INFO.status.exitstatus : 1
               end
    end
  rescue PTY::ChildExited => e
    # The child process exited
    last_exception = e
    status = e.status
  end
  [last_exception, status]
end

if __FILE__ == $PROGRAM_NAME
  if ARGV.length > 0
    run_command_with_retry ARGV
  else
    puts "Usage: with_retry.rb command --and your --args of choice"
    exit 1
  end
end
